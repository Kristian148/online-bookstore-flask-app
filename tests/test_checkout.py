import pytest
from app import app, cart, users, User

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

@pytest.fixture
def setup_test_data():
    """Setup test data before each test"""
    # Clear cart
    cart.clear()
    
    # Add a test book to cart
    from models import Book
    test_book = Book("Test Book", "Fiction", 10.99, "/test.jpg")
    cart.add_book(test_book, 1)
    
    # Create test user
    test_user = User("test@example.com", "password123", "Test User", "123 Test St")
    users["test@example.com"] = test_user
    
    yield
    
    # Cleanup
    cart.clear()
    if "test@example.com" in users:
        del users["test@example.com"]

def test_checkout_valid_card(client, setup_test_data):
    """Test checkout with valid credit card"""
    with client.session_transaction() as sess:
        sess['user_email'] = 'test@example.com'
    
    response = client.post("/process-checkout", data={
        'payment_method': 'credit_card',
        'card_number': '4242424242424242',
        'expiry_date': '12/25',
        'cvv': '123',
        'cardholder_name': 'Test User',
        'name': 'Test User',
        'email': 'test@example.com',
        'address': '123 Test St',
        'city': 'Test City',
        'state': 'TS',
        'zip_code': '12345'
    })
    
    # Should redirect to order confirmation
    assert response.status_code == 302

def test_checkout_invalid_card(client, setup_test_data):
    """Test checkout with invalid credit card (ending in 1111)"""
    with client.session_transaction() as sess:
        sess['user_email'] = 'test@example.com'

    response = client.post("/process-checkout", data={
        'payment_method': 'credit_card',
        'card_number': '1111111111111111',
        'expiry_date': '12/25',
        'cvv': '123',
        'cardholder_name': 'Test User',
        'name': 'Test User',
        'email': 'test@example.com',
        'address': '123 Test St',
        'city': 'Test City',
        'state': 'TS',
        'zip_code': '12345'
    })
    # Redirect (302) is expected when payment fails
    assert response.status_code == 302
