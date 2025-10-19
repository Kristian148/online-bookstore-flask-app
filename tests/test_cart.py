from app import app

def test_add_to_cart():
    client = app.test_client()
    response = client.post('/add-to-cart', data={'title': 'Book Title', 'quantity': 1})
    assert response.status_code in [200, 302]

from app import app

def test_update_cart_quantity():
    client = app.test_client()

    # Step 1: Add a book to the cart first
    client.post('/add-to-cart', data={'title': 'The Great Gatsby', 'quantity': 1})

    # Step 2: Update the quantity for that same book
    response = client.post('/update-cart', data={'title': 'The Great Gatsby', 'quantity': 3})

    # Step 3: Verify the request succeeded (expecting redirect)
    assert response.status_code == 302, "Expected redirect after cart update"

    # Step 4: Follow the redirect to get the final page with flash message
    final_response = client.get(response.location)
    assert b'Updated' in final_response.data or b'success' in final_response.data

from app import app

from app import cart  # import the cart instance

def test_remove_zero_quantity_item():
    client = app.test_client()

    # Reset the cart before starting this test
    cart.clear()

    # Add an item to cart
    client.post('/add-to-cart', data={'title': 'Moby Dick', 'quantity': 1})

    # Update quantity to zero (should remove item)
    response = client.post('/update-cart', data={'title': 'Moby Dick', 'quantity': 0}, follow_redirects=True)
    page = response.get_data(as_text=True)

    assert response.status_code == 200
    assert 'your cart is empty' in page.lower(), "Cart not empty message not found"



from app import app

def test_clear_cart():
    client = app.test_client()
    # Add a book first
    client.post('/add-to-cart', data={'title': 'The Great Gatsby', 'quantity': 1})
    # Then clear the cart
    response = client.post('/clear-cart', follow_redirects=True)
    # Expect redirect or empty cart page
    assert response.status_code in [200, 302]
    assert b'Cart' in response.data or b'Empty' in response.data
