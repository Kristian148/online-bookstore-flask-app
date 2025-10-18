# AI Agent Instructions for Online Bookstore Flask Application

## 🎯 Project Purpose

This is an **educational Flask e-commerce application** designed for software testing learning. It **intentionally contains bugs and inefficiencies** to provide realistic testing scenarios. When working on this codebase, understand that some issues are deliberately introduced for educational purposes.

## 🏗️ Architecture Overview

### Core Design Patterns
- **Single-file Flask app** (`app.py`) with route handlers and business logic
- **Model classes** (`models.py`) using plain Python classes (no ORM)
- **In-memory storage** with global dictionaries (`users`, `orders`)
- **Mock services** for payment processing and email notifications
- **Session-based** cart and authentication management

### Key Components
- `Cart`: Dictionary-based cart using book titles as keys (`self.items = {}`)
- `User`: Plain class with order history tracking (`self.orders = []`)
- `PaymentGateway`: Mock service with deliberate failure scenarios (cards ending in '1111')
- `EmailService`: Console-output simulation for order confirmations

## 🔄 Critical Data Flow

### Cart Operations
```python
# Cart uses book title as dictionary key for lookups
cart.items[book.title] = CartItem(book, quantity)
```

### User Session Management
```python
# Session stores user email, not user object
session['user_email'] = email
# Retrieve user via global users dict
user = users.get(session['user_email'])
```

### Order Processing Chain
1. **Checkout form** → `process_checkout()` route
2. **Payment validation** → `PaymentGateway.process_payment()`
3. **Order creation** → Store in global `orders` dict
4. **Email notification** → `EmailService.send_order_confirmation()`

## 🚨 Known Intentional Issues

When fixing bugs, check `INSTRUCTOR_BUGS_LIST.md` to verify if an issue is intentionally educational:

### Performance Inefficiencies
- `Cart.get_total_price()` uses nested loops instead of simple multiplication
- Linear search patterns instead of dictionary lookups
- Unnecessary sorting operations (`user.orders.sort()`)

### Input Validation Gaps
- Missing try-catch around `int(request.form.get('quantity'))`
- No email format validation in registration
- Case-sensitive discount codes (`'SAVE10'` exact match required)

### Security Vulnerabilities
- Plain text password storage
- Case-sensitive email checking allows duplicate accounts
- Missing input sanitization

## 🧪 Testing Patterns

### Test Account Available
```python
# Pre-created demo user for testing
demo_user = User("demo@bookstore.com", "demo123", "Demo User", ...)
```

### Payment Test Scenarios
```python
# Cards ending in '1111' trigger payment failures
# All other card numbers succeed
# PayPal payments have minimal validation
```

### Running Tests
```bash
# Install dependencies
pip install -r requirements.txt

# Run existing tests
pytest tests/

# Run Flask app for manual testing
python app.py  # Runs on http://localhost:5000
```

## 🛠️ Development Workflows

### Adding New Features
1. **Models first**: Add classes to `models.py` if new data structures needed
2. **Routes**: Add Flask routes to `app.py` following existing patterns
3. **Templates**: Create/modify Jinja2 templates in `templates/`
4. **Session handling**: Use existing session patterns for state management

### Common Debugging
```python
# Check cart contents
print(f"Cart items: {cart.items}")

# Verify user session
print(f"Current user: {session.get('user_email')}")

# Debug payment processing
print(f"Payment result: {PaymentGateway.process_payment(payment_info)}")
```

### Template Context
- Most templates expect `cart` object for cart item display
- User authentication state checked via `session['user_email']`
- Flash messages use categories: `'success'`, `'error'`

## 📁 Key Files to Understand

- **`app.py`**: All routes, session management, and business logic
- **`models.py`**: Data classes and mock service implementations
- **`INSTRUCTOR_BUGS_LIST.md`**: Catalog of intentional issues (educational context)
- **`templates/checkout.html`**: Complex form with payment method switching
- **`static/styles.css`**: Responsive design patterns

## 🔍 Code Conventions

### Route Naming
- GET routes: noun-based (`/cart`, `/checkout`)
- POST routes: action-based (`/add-to-cart`, `/process-checkout`)

### Error Handling
```python
# Standard flash message pattern
flash('Error message', 'error')
return render_template('template.html')
```

### Helper Functions
- `get_book_by_title()`: Find book in global BOOKS list
- `get_current_user()`: Get user from session
- `@login_required`: Decorator for protected routes

This codebase prioritizes educational value over production patterns. When suggesting improvements, consider whether changes align with the teaching objectives around testing and debugging scenarios.