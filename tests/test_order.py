from app import app, users, cart
from models import User

def test_order_confirmation_flow():
    client = app.test_client()

    # Ensure clean state
    users.clear()
    cart.clear()

    # Create a demo user and log them in
    demo_user = User("demo@bookstore.com", "demo123", "Demo User", "123 Demo St")
    users["demo@bookstore.com"] = demo_user
    client.post(
        "/login",
        data={"email": "demo@bookstore.com", "password": "demo123"},
        follow_redirects=True,
    )

    # Add an item to the cart
    client.post("/add-to-cart", data={"title": "The Great Gatsby", "quantity": 1})

    # Proceed to checkout with valid payment
    response = client.post(
        "/process-checkout",
        data={
            "name": "Demo User",
            "email": "demo@bookstore.com", 
            "address": "123 Test St",
            "city": "Test City",
            "zip_code": "12345",
            "payment_method": "credit_card",
            "card_number": "1234567890123456",  # Valid card
            "expiry_date": "12/25",
            "cvv": "123"
        },
        follow_redirects=True,
    )
    page = response.get_data(as_text=True)

    # Check that the confirmation page is shown
    assert response.status_code == 200
    assert "order" in page.lower() and ("confirmed" in page.lower() or "thank you" in page.lower())

    # Optional: ensure the cart is now empty
    assert cart.is_empty(), "Cart was not cleared after order confirmation"
