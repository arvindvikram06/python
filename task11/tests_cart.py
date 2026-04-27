"""
Cart and checkout tests demonstrating the miniest testing framework.
"""

from miniest import (
    main, parametrize, skip,
    assert_equal, TestFramework, AssertionError
)


@parametrize((1, 1), (2, 5), (99, 0))
def test_add_item(product_id, qty):
    """Test adding items with different product IDs and quantities."""
    assert product_id > 0, "Product ID must be positive"
    assert qty >= 0, "Quantity must be non-negative"


@parametrize((2, 5), (5, 1), (10, 10))
def test_add_item_different_combos(product_id, qty):
    """Test different product/quantity combinations."""
    total = product_id * qty
    assert total > 0, "Total should be positive"


def test_cart_empty():
    """Test empty cart."""
    cart = []
    assert_equal(len(cart), 0, "Cart should be empty")


def test_cart_add_items():
    """Test adding items to cart."""
    cart = []
    cart.append({"id": 1, "qty": 2})
    cart.append({"id": 2, "qty": 3})
    assert_equal(len(cart), 2, "Cart should have 2 items")


def test_cart_total():
    """Test cart total price calculation."""
    items = [
        {"id": 1, "price": 10.0, "qty": 2},
        {"id": 2, "price": 5.0, "qty": 3}
    ]
    total = sum(item["price"] * item["qty"] for item in items)
    assert_equal(total, 35.0, "Total should be 35.0")


def test_discount_calculation():
    """Test discount calculation."""
    original_price = 100.0
    discount_percent = 10
    final_price = original_price * (1 - discount_percent / 100)
    assert_equal(final_price, 90.0, "Final price should be 90.0")


@skip("no API key")
def test_checkout_stripe():
    """Test checkout with Stripe payment."""
    pass


@skip()
def test_payment_gateway():
    """Test payment gateway."""
    pass


def test_payment_validation():
    """Test payment validation."""
    amount = 100.0
    assert amount > 0, "Amount should be positive"
    assert amount < 10000.0, "Amount should be reasonable"


def test_order_confirmation():
    """Test order confirmation."""
    order_id = 12345
    status = "confirmed"
    assert_equal(status, "confirmed")
    assert order_id > 0 and order_id < 100000


if __name__ == "__main__":
    framework = TestFramework()
    import sys
    results = framework.run(sys.modules[__name__], parallel=1, verbose=True)
