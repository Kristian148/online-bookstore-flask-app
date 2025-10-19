from app import app

def test_checkout_with_empty_cart_blocked():
    client = app.test_client()

    # Step 1: Attempt checkout with no items
    response = client.get('/checkout', follow_redirects=True)
    page = response.get_data(as_text=True)

    # Step 2: Verify checkout is blocked
    assert response.status_code == 200
    assert "empty" in page.lower() or "add items" in page.lower(), \
        "Checkout proceeded despite empty cart"
