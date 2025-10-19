import timeit
from models import Cart
from app import Book

def test_large_cart_checkout_performance():
    cart = Cart()

    # Add 500 books to simulate a large user cart
    for i in range(500):
        cart.add_book(Book(f"Book {i}", "Fiction", 9.99, ""), quantity=3)

    # Measure execution time of total price calculation
    execution_time = timeit.timeit(lambda: cart.get_total_price(), number=50)
    print(f"Checkout simulation (500 items) took: {execution_time:.4f}s")

    # Assert performance threshold
    assert execution_time < 2.0, f"Checkout too slow ({execution_time:.2f}s)"

import timeit
from models import Cart
from app import Book

def test_cart_calculation_efficiency():
    cart = Cart()

    # Add 1000 books to simulate a larger cart
    for i in range(1000):
        cart.add_book(Book(f"Book {i}", "Fiction", 9.99, ""), quantity=1)

    # Time the total price calculation
    exec_time = timeit.timeit(lambda: cart.get_total_price(), number=50)
    print(f"Cart total efficiency test: {exec_time:.4f}s for 1000 items")

    # Test passes if calculation completes in under 1 second
    assert exec_time < 1.0, f"Cart calculation too slow ({exec_time:.2f}s)"
