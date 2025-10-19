import pytest
from app import app, cart, users, User
from models import PaymentGateway

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        with app.app_context():
            yield client

def test_payment_gateway_success():
    """Test payment gateway with valid card"""
    payment_info = {
        'payment_method': 'credit_card',
        'card_number': '4242424242424242',
        'expiry_date': '12/25',
        'cvv': '123',
        'cardholder_name': 'Test User'
    }
    
    result = PaymentGateway.process_payment(payment_info)
    
    assert result['success'] is True
    assert 'transaction_id' in result
    assert result['transaction_id'] is not None

def test_payment_failure_card_ending_1111():
    """Test payment gateway with card ending in 1111 (should fail)"""
    payment_info = {
        'payment_method': 'credit_card',
        'card_number': '1111111111111111',
        'expiry_date': '12/25',
        'cvv': '123',
        'cardholder_name': 'Test User'
    }
    
    result = PaymentGateway.process_payment(payment_info)
    
    assert result['success'] is False
    assert 'Invalid card number' in result['message']
    assert result['transaction_id'] is None

def test_paypal_payment():
    """Test PayPal payment processing"""
    payment_info = {
        'payment_method': 'paypal',
        'paypal_email': 'test@example.com'
    }
    
    result = PaymentGateway.process_payment(payment_info)
    
    assert result['success'] is True
    assert 'transaction_id' in result

from app import app

def test_invalid_paypal_payment():
    client = app.test_client()
    
    # Add item to cart properly
    client.post('/add-to-cart', data={'title': 'The Great Gatsby', 'quantity': 1})
    
    response = client.post('/process-checkout', data={
        'name': 'Test User',
        'email': 'test@example.com',
        'address': '123 Test St',
        'city': 'Test City', 
        'zip_code': '12345',
        'payment_method': 'paypal',
        'paypal_email': 'invalid@none.com'
    })
    assert b"error" in response.data or response.status_code in [400, 302]

