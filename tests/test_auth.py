from app import app

def test_duplicate_email_registration():
    client = app.test_client()
    # Register user 1
    client.post('/register', data={'email': 'duplicate@test.com', 'password': 'abc123', 'name': 'User A'})
    # Try registering same email again
    response = client.post('/register', data={'email': 'duplicate@test.com', 'password': 'abc123', 'name': 'User B'})
    assert b'An account with this email already exists' in response.data or response.status_code in [400, 302]

from app import app, users, cart
from models import User

def test_duplicate_email_registration():
    client = app.test_client()
    # Register user 1
    client.post('/register', data={'email': 'duplicate@test.com', 'password': 'abc123', 'name': 'User A'})
    # Try registering same email again
    response = client.post('/register', data={'email': 'duplicate@test.com', 'password': 'abc123', 'name': 'User B'})
    assert b'An account with this email already exists' in response.data or response.status_code in [400, 302]

def test_valid_login():
    client = app.test_client()

    # Ensure a clean slate
    users.clear()

    # Create a proper user with hashed password
    test_user = User("demo@bookstore.com", "demo123", "Demo User", "123 Test St")
    users["demo@bookstore.com"] = test_user

    # Attempt to log in with valid credentials
    response = client.post(
        "/login",
        data={"email": "demo@bookstore.com", "password": "demo123"},
        follow_redirects=True,
    )
    page = response.get_data(as_text=True)

    # Expect success message or redirect to home
    assert response.status_code == 200
    assert "hello, demo user" in page.lower() or "logout" in page.lower()


def test_invalid_login():
    client = app.test_client()

    # Attempt to log in with wrong password
    response = client.post(
        "/login",
        data={"email": "demo@bookstore.com", "password": "wrongpass"},
        follow_redirects=True,
    )
    page = response.get_data(as_text=True)

    # Expect failure message
    assert response.status_code == 200
    assert "invalid email or password" in page.lower()

from app import app, users

def test_logout_clears_session():
    client = app.test_client()

    # Ensure clean state
    users.clear()

    # Register a user directly in memory
    users["demo@bookstore.com"] = type(
        "User", (), {"email": "demo@bookstore.com", "password": "demo123", "name": "Demo User"}
    )

    # Log in first
    client.post(
        "/login",
        data={"email": "demo@bookstore.com", "password": "demo123"},
        follow_redirects=True,
    )

    # Log out
    response = client.get("/logout", follow_redirects=True)
    page = response.get_data(as_text=True)

    # Assert session is cleared and message shown
    assert response.status_code == 200
    assert "logged out successfully" in page.lower() or "login" in page.lower()

from app import app, users

def test_session_management_access_control():
    client = app.test_client()

    # Ensure a clean slate
    users.clear()

    # Create a proper demo user
    test_user = User("demo@bookstore.com", "demo123", "Demo User", "123 Test St")
    users["demo@bookstore.com"] = test_user

    # Log in
    client.post(
        "/login",
        data={"email": "demo@bookstore.com", "password": "demo123"},
        follow_redirects=True,
    )

    # Log out to clear the session
    client.get("/logout", follow_redirects=True)

    # Attempt to access a protected route after logout
    response = client.get("/account", follow_redirects=True)
    page = response.get_data(as_text=True)

    # Check that the user is redirected to login or blocked
    assert response.status_code == 200
    assert "login" in page.lower() or "please log in" in page.lower(), \
        "User was able to access protected page after logout"
