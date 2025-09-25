# Simple E-Commerce Backend API

A streamlined e-commerce backend built with FastAPI for **guest shopping** with **admin-only management**. Perfect for small businesses that want customers to shop without registration and receive orders via WhatsApp.

## 🚀 Features

- **Guest Shopping**: No user registration required - customers can shop immediately
- **Session-based Cart**: Shopping cart using browser sessions
- **Guest Checkout**: Simple checkout with name, phone, and address
- **WhatsApp Integration**: Orders automatically sent to admin's WhatsApp
- **Admin Dashboard**: Admin-only login for product and order management
- **Real-time Notifications**: Order status updates sent to customers via WhatsApp

## 🛠️ Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT tokens for admin only
- **Notifications**: WhatsApp API integration
- **Validation**: Pydantic models

## 🛒 Customer Flow

1. **Browse Products**: No login required
2. **Add to Cart**: Items saved by session ID
3. **Checkout**: Enter name, phone, address
4. **Order Placed**: Automatic WhatsApp to admin
5. **Status Updates**: Receive WhatsApp notifications

## 👨‍💼 Admin Flow

1. **Login**: Admin authentication required
2. **Manage Products**: Add, edit, delete products
3. **View Orders**: See all customer orders
4. **Update Status**: Change order status (triggers customer notification)
5. **Dashboard**: View sales statistics

## 📦 Quick Setup

### Option 1: Automated Setup

```bash
python setup.py
```

### Option 2: Manual Setup

1. **Create and activate virtual environment:**

```bash
python -m venv venv
venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On Linux/Mac
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Set up environment variables:**

```bash
copy .env.example .env  # On Windows
# cp .env.example .env    # On Linux/Mac
```

Edit `.env` with your database credentials.

4. **Set up PostgreSQL database:**

```sql
CREATE DATABASE ecommerce_db;
CREATE USER your_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE ecommerce_db TO your_user;
```

5. **Configure WhatsApp (Optional for development):**

   - Sign up for a WhatsApp Business API service (like Twilio, 360Dialog, etc.)
   - Update `.env` with your WhatsApp API credentials
   - For development, messages will be logged to console

6. **Run database migrations:**

```bash
alembic upgrade head
```

7. **Create first admin account:**

```bash
# Start the server first
uvicorn app.main:app --reload

# Then register admin via API or add directly to database
```

8. **Start the development server:**

```bash
uvicorn app.main:app --reload
```

## 📚 API Documentation

Once the server is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔐 Admin Authentication

### Register first admin:

```bash
POST /api/v1/auth/admin/register
{
    "username": "admin",
    "email": "admin@example.com",
    "password": "securepassword"
}
```

### Admin login:

```bash
POST /api/v1/auth/admin/login
Content-Type: application/x-www-form-urlencoded

username=admin&password=securepassword
```

### Use the token for admin operations:

```bash
Authorization: Bearer <admin_access_token>
```

## 🛒 Guest Shopping Flow

### Browse products (no auth required):

```bash
GET /api/v1/products/
```

### Add to cart (using session ID):

```bash
POST /api/v1/cart/
{
    "session_id": "unique-browser-session-id",
    "product_id": 1,
    "quantity": 2
}
```

### Guest checkout:

```bash
POST /api/v1/orders/
{
    "customer_name": "John Doe",
    "customer_phone": "+1234567890",
    "customer_address": "123 Main St, City, State",
    "session_id": "unique-browser-session-id",
    "notes": "Please ring doorbell"
}
```

## 📁 Project Structure

```
app/
├── models/         # SQLAlchemy database models
│   └── models.py   # Admin, Product, Order, Cart models
├── routers/        # FastAPI route handlers
│   ├── auth.py     # Admin authentication only
│   ├── products.py # Product and category management
│   ├── cart.py     # Guest shopping cart
│   └── orders.py   # Guest orders + admin management
├── schemas/        # Pydantic models for request/response
│   └── schemas.py  # All Pydantic schemas
├── utils/          # Utility functions and helpers
│   ├── auth.py     # JWT utilities
│   ├── dependencies.py # Admin authentication
│   ├── whatsapp.py # WhatsApp integration
│   ├── exceptions.py   # Exception handlers
│   ├── logging.py     # Logging utilities
│   └── middleware.py  # Custom middleware
├── main.py         # FastAPI application entry point
├── database.py     # Database connection and configuration
└── config.py       # Application configuration
```

## 🛡️ Security Features

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: bcrypt for secure password storage
- **Role-based Access**: Admin and user roles
- **Input Validation**: Pydantic models for request validation
- **CORS Protection**: Configurable CORS middleware

## 📊 API Endpoints

### Guest Shopping (No Authentication)

- `GET /api/v1/products/` - Browse products with filtering
- `GET /api/v1/products/{id}` - Get specific product
- `GET /api/v1/products/categories/` - Get all categories
- `GET /api/v1/cart/{session_id}` - Get cart items
- `POST /api/v1/cart/` - Add item to cart
- `PUT /api/v1/cart/{id}` - Update cart item
- `DELETE /api/v1/cart/{id}` - Remove item from cart
- `POST /api/v1/orders/` - Place order (guest checkout)
- `GET /api/v1/orders/{order_number}` - Get order status

### Admin Only (Authentication Required)

- `POST /api/v1/auth/admin/register` - Register admin
- `POST /api/v1/auth/admin/login` - Admin login
- `POST /api/v1/products/` - Create product
- `PUT /api/v1/products/{id}` - Update product
- `DELETE /api/v1/products/{id}` - Delete product
- `POST /api/v1/products/categories/` - Create category
- `GET /api/v1/orders/admin/all` - View all orders
- `PUT /api/v1/orders/admin/{id}` - Update order status
- `GET /api/v1/orders/admin/stats` - Order statistics

## 🧪 Testing

Run tests with pytest:

```bash
pytest
```

## 🚀 Production Deployment

1. **Update environment variables** for production
2. **Set up PostgreSQL** database
3. **Configure CORS** origins in `main.py`
4. **Use a production WSGI server** like Gunicorn:

```bash
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## 📝 Environment Variables

```env
DATABASE_URL=postgresql://user:password@localhost/ecommerce_db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# WhatsApp Configuration
WHATSAPP_API_URL=https://api.whatsapp-service.com/send
WHATSAPP_TOKEN=your-whatsapp-api-token
ADMIN_WHATSAPP_NUMBER=+1234567890

DEBUG=False
ENVIRONMENT=production
```

## 📱 WhatsApp Integration

This system integrates with WhatsApp to:

1. **Send order notifications to admin** when customers place orders
2. **Send status updates to customers** when admin changes order status

### Supported WhatsApp Services:

- Twilio WhatsApp API
- 360Dialog
- WhatsApp Business API
- Any service with REST API

### Development Mode:

- Without WhatsApp credentials, messages are logged to console
- Perfect for testing without actual WhatsApp integration

## 🎯 Perfect For:

- **Small Restaurants**: Take orders without customer registration
- **Local Shops**: Simple online ordering with WhatsApp notifications
- **Service Businesses**: Easy booking system with admin management
- **Pop-up Stores**: Quick setup without complex user management

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.
