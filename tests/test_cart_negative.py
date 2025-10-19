from app import app

def test_negative_quantity_rejected():
    client = app.test_client()

    # Step 1: Add a valid book to cart
    client.post('/add-to-cart', data={'title': 'The Great Gatsby', 'quantity': 1})

    # Step 2: Try updating to an invalid negative quantity
    response = client.post('/update-cart', data={'title': 'The Great Gatsby', 'quantity': -3}, follow_redirects=True)
    page = response.get_data(as_text=True)

    # Step 3: Validate correct handling
    assert response.status_code == 200
    assert "removed" in page.lower() or "invalid" in page.lower() or "empty" in page.lower(), \
        "Negative quantity not handled properly"
