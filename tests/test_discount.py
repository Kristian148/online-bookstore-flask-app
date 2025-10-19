from app import app, cart

def test_discount_code_case_insensitivity():
    client = app.test_client()
    
    # Clear cart for clean test
    cart.clear()

    # Step 1: Add an item to cart first
    client.post('/add-to-cart', data={'title': 'The Great Gatsby', 'quantity': 1})

    # Step 2: Process checkout with lowercase discount code (should still work)
    response = client.post('/process-checkout', data={
        'name': 'Test User',
        'email': 'test@example.com',
        'address': '123 Test St',
        'city': 'Test City',
        'zip_code': '12345',
        'payment_method': 'credit_card',
        'card_number': '1234567890123456',
        'expiry_date': '12/25',
        'cvv': '123',
        'discount_code': 'save10'  # lowercase
    }, follow_redirects=True)
    page = response.get_data(as_text=True)

    # Step 3: Check that discount was applied successfully
    assert response.status_code == 200
    # Check that the discounted price appears (10.99 - 10% = 9.89)  
    assert "$9.89" in page, "Discount not applied for lowercase code — case-sensitive bug"
