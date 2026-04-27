"""
Example tests demonstrating the miniest testing framework.
"""

from miniest import (
    TestFramework, AssertionError, assert_equal
)

# Create a test framework instance
_framework = TestFramework()

# Register fixtures with this instance
@_framework.fixture_manager.fixture(scope="function")
def temp_dir():
    """Function-scoped fixture for temporary directory."""
    import tempfile
    import os
    tmpdir = tempfile.mkdtemp()
    # Cleanup
    import shutil
    try:
        shutil.rmtree(tmpdir)
    except:
        pass
    return tmpdir


@_framework.fixture_manager.fixture(scope="session")
def db_connection():
    """Session-scoped fixture for database connection."""
    return {"type": "mock_db", "connected": True}


def parametrize(*params):
    """Decorator to parametrize tests."""
    from miniest import ParametrizedTest
    return ParametrizedTest(params)


def skip(reason: str = ""):
    """Decorator to skip a test."""
    def decorator(func):
        func._skip = True
        func._skip_reason = reason
        return func
    return decorator


# ============= SIMPLE TESTS =============
def test_login_valid_credentials():
    """Test valid login."""
    username = "admin"
    password = "password123"
    assert_equal(username, "admin", "Username should be admin")
    assert_equal(len(password), 11, "Password should be 11 chars")


def test_login_invalid_password():
    """Test invalid password login."""
    status = 200
    try:
        assert_equal(status, 401)
        assert False, "Should have failed"
    except AssertionError:
        pass  # Expected


def test_login_expired_token():
    """Test expired token."""
    status = 200
    try:
        assert_equal(status, 401)
    except AssertionError as e:
        assert "Expected 401" in str(e)


# ============= PARAMETRIZED TESTS =============
@parametrize((1, 1), (2, 5), (99, 0))
def test_add_item(product_id, qty):
    """Test add item with parametrized values."""
    assert product_id > 0, f"Product ID {product_id} should be positive"
    assert qty >= 0, f"Quantity {qty} should be non-negative"


@parametrize((2, 5), (5, 1))
def test_add_item_parametrized(product_id, qty):
    """Another parametrized test."""
    result = product_id * qty
    assert result > 0, f"Result should be positive"


# ============= SKIPPED TESTS =============
@skip("no API key")
def test_checkout_stripe():
    """Test checkout with Stripe (skipped)."""
    pass


@skip()
def test_payment_gateway():
    """Test payment gateway (skipped)."""
    pass


# ============= FIXTURE INJECTION TESTS =============
def test_with_db_connection(db_connection):
    """Test with database connection fixture."""
    assert_equal(db_connection["type"], "mock_db")
    assert db_connection["connected"] is True


# ============= INTEGRATION TESTS =============
def test_full_integration():
    """Integration test using multiple assertions."""
    user_id = 42
    user_name = "Alice"
    age = 30
    
    assert_equal(user_id, 42)
    assert_equal(user_name, "Alice")
    assert_equal(age, 30)


def test_string_operations():
    """Test string operations."""
    text = "Hello World"
    assert_equal(text.upper(), "HELLO WORLD")
    assert_equal(len(text), 11)


def test_list_operations():
    """Test list operations."""
    items = [1, 2, 3, 4, 5]
    assert_equal(len(items), 5)
    assert_equal(items[0], 1)
    assert_equal(sum(items), 15)


if __name__ == "__main__":
    # Run tests with the framework
    import sys
    results = _framework.run(sys.modules[__name__], parallel=1, verbose=True)
