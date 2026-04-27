# Task 11: Automated Testing Framework

A miniature test framework built from scratch with all the essentials for testing Python code.

## Features

### 1. **Test Discovery**
- Automatic discovery of test functions by naming convention (`test_*`)
- Functions must be named starting with `test_`

### 2. **Fixtures**
- Setup and teardown support with different scopes:
  - **function**: Created/destroyed for each test
  - **session**: Created once for the entire session
  - **module**: Created once per module

### 3. **Parametrized Tests**
- Run the same test with multiple input sets
- Use `@parametrize()` decorator with parameter tuples
- Each parameter combination runs separately

### 4. **Assertion Introspection**
- Detailed assertion messages showing expected vs actual values
- Custom `assert_equal()` function with formatted diff
- Traceback and exception handling for debugging

### 5. **Parallel Execution**
- Run tests in parallel using `multiprocessing.Pool`
- Configurable number of worker processes
- Sequential execution with `parallel=1` (default)

## Architecture

### Core Components

1. **TestFramework**: Main orchestrator
   - `discover_tests()`: Finds all test functions
   - `run_test()`: Executes a single test
   - `run_tests()`: Executes multiple tests
   - `run()`: Main entry point

2. **TestFixture**: Fixture management
   - Caches fixtures by scope
   - Handles setup/teardown lifecycle

3. **TestResult**: Stores test execution data
   - Test name, status (PASS/FAIL/SKIP)
   - Execution time
   - Error messages

4. **Decorators**:
   - `@fixture(scope)`: Define fixtures
   - `@parametrize()`: Parametrize tests
   - `@skip()`: Skip tests with optional reason

## Usage

### Basic Test
```python
from miniest import assert_equal, TestFramework

def test_example():
    assert_equal(1 + 1, 2)

# Run tests
framework = TestFramework()
results = framework.run(__import__('__main__'))
```

### With Fixtures
```python
from miniest import fixture, TestFramework

@fixture(scope="function")
def db_connection():
    yield {"type": "mock_db"}

def test_with_fixture(db_connection):
    assert db_connection["type"] == "mock_db"
```

### Parametrized Tests
```python
from miniest import parametrize

@parametrize((1, 2), (3, 4), (5, 6))
def test_values(a, b):
    assert a < b
```

### Skipped Tests
```python
from miniest import skip

@skip("not ready")
def test_future_feature():
    pass
```

## Running Tests

```bash
# Run tests_auth.py
cd task11
python -c "from tests_auth import *; from miniest import TestFramework; import sys; TestFramework().run(sys.modules[__name__], verbose=True)"

# Or directly
python tests_auth.py

# Parallel execution with 4 workers
python -c "from tests_auth import *; from miniest import TestFramework; import sys; TestFramework().run(sys.modules[__name__], parallel=4, verbose=True)"
```

## Test Examples

### Authentication Tests (`tests_auth.py`)
- Valid/invalid login
- Expired token handling
- Fixture injection for database connections
- Mixed PASS/FAIL/SKIP tests

### Cart Tests (`tests_cart.py`)
- Parametrized cart operations
- Price calculations with discount
- Order confirmation
- Skipped payment gateway tests

## Output

```
=== Test Discovery ===
Found 12 tests

=== Execution ===
  ✓ test_login_valid_credentials [0.01s]
  ✗ test_login_expired_token [0.02s]
  ⊘ test_checkout_stripe [0.00s]
  ...

=== Summary ===
12 tests | 10 passed | 1 failed | 1 skipped
Total time: 0.48s
```

## Implementation Details

### Test Discovery
- Uses `inspect.getmembers()` to find functions in module
- Filters by name prefix `test_`
- Returns sorted list for consistent execution order

### Fixture Management
- Fixtures are cached by `(name, scope)` tuple
- Function-scoped fixtures cleared after each test
- Session-scoped fixtures persist for entire run

### Assertion Introspection
- Custom `AssertionError` with formatted diff
- Shows expected, actual, and differences
- Includes traceback for debugging

### Parallel Execution
- Uses `multiprocessing.Pool` for worker management
- Each test runs independently in a worker process
- Results collected and printed with summary

## Prerequisites

- Python 3.6+
- Standard library modules:
  - `inspect` - Function/module introspection
  - `traceback` - Exception formatting
  - `contextlib` - Context managers
  - `multiprocessing` - Parallel execution
  - `functools` - Decorators
  - `time` - Timing measurements

## Key Learnings

1. **Decorators**: Using closures for flexible test configuration
2. **Introspection**: Finding and analyzing functions at runtime
3. **Context Managers**: Managing resource lifecycle
4. **Multiprocessing**: Parallel execution challenges
5. **Error Formatting**: User-friendly assertion messages
