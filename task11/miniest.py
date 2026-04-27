"""
Automated Testing Framework - Miniature test framework with test discovery,
fixtures, parametrized tests, assertion introspection, and parallel execution.
"""

import inspect
import traceback
from contextlib import contextmanager
from multiprocessing import Pool
from functools import wraps
from typing import Any, Callable, Dict, List, Tuple, Optional
import time


class AssertionError(Exception):
    """Custom assertion error with formatted diff."""
    pass


class TestFixture:
    """Manager for test fixtures with different scopes."""
    
    def __init__(self):
        self.fixtures = {}
        self.scope_cache = {}
    
    def fixture(self, scope="function"):
        """Decorator to define a fixture."""
        def decorator(func):
            self.fixtures[func.__name__] = (func, scope)
            return func
        return decorator
    
    def get_fixture(self, name: str, scope: str):
        """Get or create a fixture."""
        cache_key = (name, scope)
        if cache_key not in self.scope_cache:
            if name in self.fixtures:
                func, _ = self.fixtures[name]
                if inspect.isgeneratorfunction(func):
                    self.scope_cache[cache_key] = next(func())
                else:
                    self.scope_cache[cache_key] = func()
        return self.scope_cache.get(cache_key)
    
    def clear_function_scope(self):
        """Clear function-scoped fixtures."""
        to_remove = [k for k in self.scope_cache if k[1] == "function"]
        for k in to_remove:
            del self.scope_cache[k]



# for test results
class TestResult:
    """Represents a single test result."""
    
    def __init__(self, name: str, status: str, time: float = 0, message: str = ""):
        self.name = name
        self.status = status  # PASS, FAIL, SKIP
        self.time = time
        self.message = message


# to store the parameters provided
class ParametrizedTest:
    """Decorator for parametrized tests."""
    
    def __init__(self, params: List[Any]):
        self.params = params
    
    def __call__(self, func):
        func._parametrize = self.params
        return func


def parametrize(*params):
    """Decorator to parametrize tests."""
    return ParametrizedTest(params)


def skip(reason: str = ""):
    """Decorator to skip a test."""
    def decorator(func):
        func._skip = True
        func._skip_reason = reason
        return func
    return decorator


def assert_equal(actual: Any, expected: Any, message: str = ""):
    """Assert that actual equals expected with detailed diff."""
    if actual != expected:
        diff = format_assertion_diff(actual, expected)
        error_msg = f"Expected {expected}, got {actual}\n{diff}"
        if message:
            error_msg = f"{message}\n{error_msg}"
        raise AssertionError(error_msg)


def format_assertion_diff(actual: Any, expected: Any) -> str:
    """Format assertion difference for readability."""
    lines = []
    lines.append("Assertion failed:")
    lines.append(f"  Expected: {expected!r}")
    lines.append(f"  Actual:   {actual!r}")
    if isinstance(actual, (int, float)) and isinstance(expected, (int, float)):
        diff = abs(actual - expected)
        lines.append(f"  Difference: {diff}")
    return "\n".join(lines)


class TestFramework:
    """Main test framework with discovery, fixtures, and parallel execution."""
    
    def __init__(self):
        self.fixture_manager = TestFixture() # initialize fixtures for test
        self.tests = [] 
        self.results = []
    
    def discover_tests(self, module=None) -> List[Tuple[str, Callable]]: # finds all function starts with test_funcname
        """Discover tests in a module by naming convention."""
        if module is None:
            import sys
            module = sys.modules['__main__']
        
        tests = []
        print("in discover tests")
        for name, obj in inspect.getmembers(module):
            if name.startswith('test_') and callable(obj):
                # print(f"this is name {name} and this is func {obj}")
                tests.append((name, obj))
        
        return sorted(tests, key=lambda x: x[0])
    
    def run_test(self, test_name: str, test_func: Callable) -> TestResult:
        """Run a single test with timing and error handling."""
        start_time = time.time()
        
        # Check if test is skipped
        if hasattr(test_func, '_skip') and test_func._skip:
            reason = getattr(test_func, '_skip_reason', '')
            return TestResult(test_name, "SKIP", time.time() - start_time, reason)
        
        # Handle parametrized tests
        if hasattr(test_func, '_parametrize'):
            params = test_func._parametrize
            results = []
            for param_set in params:
                try:
                    if isinstance(param_set, (list, tuple)):
                        test_func(*param_set)
                    else:
                        test_func(param_set)
                    results.append(True)
                except Exception as e:
                    results.append((False, str(e)))
            
            if all(results):
                elapsed = time.time() - start_time
                return TestResult(test_name, "PASS", elapsed)
            else:
                failures = [r[1] for r in results if isinstance(r, tuple)] #picks only error messages from the result
                elapsed = time.time() - start_time
                return TestResult(
                    test_name, "FAIL", elapsed,
                    f"Parametrized test failures:\n" + "\n".join(failures)
                )
        
        try:
            # Get function signature to inject fixtures
            sig = inspect.signature(test_func)
            kwargs = {}
            for param_name in sig.parameters:
                if param_name in self.fixture_manager.fixtures:
                    fixture_result = self.fixture_manager.get_fixture(param_name, "function")
                    if fixture_result is not None:
                        kwargs[param_name] = fixture_result
            
            test_func(**kwargs)
            elapsed = time.time() - start_time
            return TestResult(test_name, "PASS", elapsed)
        
        except AssertionError as e:
            elapsed = time.time() - start_time
            return TestResult(test_name, "FAIL", elapsed, str(e))
        except Exception as e:
            elapsed = time.time() - start_time
            tb = traceback.format_exc()
            return TestResult(test_name, "FAIL", elapsed, tb)
        finally:
            self.fixture_manager.clear_function_scope()
    
    def run_tests(self, tests: List[Tuple[str, Callable]], parallel: int = 1) -> List[TestResult]:
        """Run tests sequentially or in parallel."""
        if parallel > 1:
            # Parallel execution using multiprocessing
            with Pool(processes=parallel) as pool:
                results = pool.starmap(self.run_test, tests)
        else:
            # Sequential execution
            results = [self.run_test(test_name, test_func) for test_name, test_func in tests]
        
        return results
    
    def print_summary(self, results: List[TestResult]):
        """Print test execution summary."""
        passed = sum(1 for r in results if r.status == "PASS")
        failed = sum(1 for r in results if r.status == "FAIL")
        skipped = sum(1 for r in results if r.status == "SKIP")
        total_time = sum(r.time for r in results)
        
        print(f"\n=== Summary ===")
        print(f"{len(results)} tests | {passed} passed | {failed} failed | {skipped} skipped")
        time_display = f"{total_time*1000:.2f}ms" if total_time < 1 else f"{total_time:.2f}s"
        print(f"Total time: {time_display}")
        
        if failed > 0:
            print("\nFailed tests:")
            for r in results:
                if r.status == "FAIL":
                    time_ms = r.time * 1000
                    print(f"  FAIL {r.name} [{time_ms:.2f}ms]")
                    if r.message:
                        print(f"    {r.message}")
        
        if skipped > 0:
            print("\nSkipped tests:")
            for r in results:
                if r.status == "SKIP":
                    print(f"  SKIP {r.name}: {r.message}")
    
    def run(self, module=None, parallel: int = 1, verbose: bool = True):
        """Main entry point to discover and run tests."""
        tests = self.discover_tests(module)
        
        if verbose:
            print(f"=== Test Discovery ===")
            print(f"Found {len(tests)} tests")
        
        results = self.run_tests(tests, parallel=parallel)
        
        if verbose:
            print(f"\n=== Execution ===")
            for result in results:
                status_symbol = "✓" if result.status == "PASS" else "✗" if result.status == "FAIL" else "⊘"
                time_ms = result.time * 1000
                print(f"  {status_symbol} {result.name} [{time_ms:.2f}ms]")
            
            self.print_summary(results)
        
        return results


# Global test framework instance
_framework = TestFramework()

# Convenience functions
fixture = _framework.fixture_manager.fixture
parametrize = parametrize


def main(module=None, parallel: int = 1, verbose: bool = True):
    """Main function to run tests."""
    return _framework.run(module, parallel=parallel, verbose=verbose)
