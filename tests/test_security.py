from models import User

def test_password_hashing():
    u = User("test@x.com", "password123", "Test")
    assert "password" not in u.password.lower(), "Password stored in plaintext!"

from app import app

def test_input_sanitization():
    client = app.test_client()
    malicious_input = "<script>alert('xss')</script>"
    response = client.post('/register', data={
        'email': malicious_input,
        'password': 'test123',
        'name': 'EvilUser'
    })
    assert b"<script>" not in response.data

from app import app

def test_duplicate_email_case_insensitive():
    client = app.test_client()

    # Register with lowercase email
    client.post('/register', data={'email': 'demo@bookstore.com', 'password': 'abc123', 'name': 'UserA'})
    
    # Attempt same email in uppercase (should be treated as duplicate)
    response = client.post('/register', data={'email': 'Demo@Bookstore.com', 'password': 'xyz789', 'name': 'UserB'})
    
    page = response.get_data(as_text=True)
    assert response.status_code in [200, 302]
    assert "exists" in page.lower() or "already registered" in page.lower(), "Case-insensitive duplicate email accepted"
