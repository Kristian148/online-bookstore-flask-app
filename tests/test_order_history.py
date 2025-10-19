from app import app

def test_order_history_display():
    client = app.test_client()

    # Step 1: Simulate a logged-in user
    with client.session_transaction() as sess:
        sess['user_email'] = 'demo@bookstore.com'  # demo user from app.py

    # Step 2: Access the account page (where order history should be visible)
    response = client.get('/account', follow_redirects=True)
    page = response.get_data(as_text=True)

    # Step 3: Validate correct status and expected content
    assert response.status_code == 200
    assert "order" in page.lower() or "history" in page.lower(), \
        "Order history not displayed correctly"
