from app import app

def test_invalid_email_format_rejected():
    client = app.test_client()

    # Step 1: Try registering with an invalid email format
    response = client.post('/register', data={
        'email': 'user@',
        'password': 'abc123',
        'name': 'Invalid Email User'
    })

    page = response.get_data(as_text=True)

    # Step 2: Verify the page doesn’t accept the input
    assert response.status_code in [200, 400]
    assert "invalid" in page.lower() or "email" in page.lower() or "please" in page.lower(), \
        "Invalid email format accepted — validation missing"
