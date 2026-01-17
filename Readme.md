# E-Commerce Platform

A full-featured e-commerce platform built with Django REST Framework and Tailwind CSS, featuring role-based access control for Admin, Supplier, Customer, and Delivery personnel.

## 🚀 Features

### User Roles
- **Admin** - Full system management, order assignment, analytics dashboard
- **Supplier** - Product inventory management, stock monitoring
- **Customer** - Product browsing, shopping cart, order placement
- **Delivery Personnel** - Delivery tracking and status updates

### Key Functionality
- 🔐 JWT-based authentication with role-based access control
- 📦 Product catalog with categories, images, and stock tracking
- 🛒 Order management system with real-time status updates
- 🚚 Delivery assignment and tracking
- 📊 Role-specific dashboards with statistics
- 💰 Dynamic pricing calculations
- 📱 Responsive design with Tailwind CSS

## 🛠️ Tech Stack

**Backend:**
- Django 4.2.0
- Django REST Framework 3.14.0
- Django REST Framework SimpleJWT 5.2.2
- Django Filter 23.1
- DRF Spectacular (API documentation)

**Frontend:**
- Django Templates (Jinja2)
- Tailwind CSS
- Vanilla JavaScript

**Database:**
- SQLite (Development)

## 📋 Prerequisites

- Python 3.8+
- pip
- virtualenv (recommended)

## ⚙️ Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd "Internship Folder"
```

2. **Create and activate virtual environment**
```bash
python -m venv .venv

# On macOS/Linux:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run migrations**
```bash
python manage.py migrate
```

5. **Create a superuser**
```bash
python manage.py createsuperuser
```

6. **Run the development server**
```bash
python manage.py runserver
```

7. **Access the application**
- Web Interface: http://127.0.0.1:8000/
- Admin Panel: http://127.0.0.1:8000/admin/
- API Documentation: http://127.0.0.1:8000/api/schema/swagger-ui/

## 📁 Project Structure

```
.
├── ecommerce/          # Main project settings
├── users/              # User authentication & authorization
├── products/           # Product management
├── orders/             # Order processing
├── delivery/           # Delivery tracking
├── notifications/      # Notification system
├── frontend/           # Frontend views & templates
├── templates/          # HTML templates
├── static/             # Static files (CSS, JS, images)
├── media/              # User-uploaded files
├── manage.py           # Django management script
└── requirements.txt    # Python dependencies
```

## 🔑 Authentication System

### JWT Token-based Authentication
- **Access Token:** 1 hour lifetime
- **Refresh Token:** 7 days lifetime
- **Token Type:** Bearer

### API Authentication
```bash
# Login to get tokens
POST /api/token/
{
  "username": "your_username",
  "password": "your_password"
}

# Use access token in headers
Authorization: Bearer <access_token>

# Refresh token
POST /api/token/refresh/
{
  "refresh": "<refresh_token>"
}
```

## 📱 User Roles & Permissions

### Admin
- View all products, orders, and deliveries
- Assign deliveries to delivery personnel
- Access analytics dashboard
- Manage system-wide settings

### Supplier
- Add and manage own products
- Update stock levels
- View low stock alerts
- Monitor product performance

### Customer
- Browse product catalog
- Place orders
- View order history
- Track order status

### Delivery Personnel
- View assigned deliveries
- Update delivery status
- Track delivery progress

## 🌐 API Endpoints

### Authentication
- `POST /api/token/` - Login (obtain tokens)
- `POST /api/token/refresh/` - Refresh access token
- `POST /api/register/` - User registration
- `GET /api/user-profile/` - Get user profile

### Products
- `GET /api/products/` - List all products
- `GET /api/products/{id}/` - Product details
- `POST /api/products/` - Create product (Supplier only)
- `PUT /api/products/{id}/` - Update product (Supplier only)
- `DELETE /api/products/{id}/` - Delete product (Supplier only)

### Orders
- `GET /api/orders/` - List orders (filtered by role)
- `POST /api/orders/` - Create order (Customer only)
- `GET /api/orders/{id}/` - Order details
- `PATCH /api/orders/{id}/` - Update order status

### Deliveries
- `GET /api/deliveries/` - List deliveries
- `POST /api/deliveries/` - Create delivery assignment (Admin only)
- `PATCH /api/deliveries/{id}/` - Update delivery status

## 🎨 Frontend Pages

### Public Pages
- `/login/` - User login
- `/register/` - User registration

### Customer Pages
- `/` - Product listing
- `/products/{id}/` - Product detail page
- `/orders/` - Order history

### Dashboards
- `/dashboard/admin/` - Admin dashboard
- `/dashboard/supplier/` - Supplier dashboard
- `/dashboard/delivery/` - Delivery dashboard

## 🔒 Security Features

- CSRF protection on all forms
- JWT token authentication
- Password hashing (Django's built-in bcrypt)
- Role-based access control
- Session management
- Automatic token refresh

## 🧪 Management Commands

### Assign User Groups
```bash
python manage.py assign_user_groups
```

### Update User Role
```bash
python manage.py update_user_role <username> <role>
```

## 🚀 Deployment Considerations

1. **Environment Variables**
   - Set `DEBUG=False` in production
   - Configure `SECRET_KEY`
   - Set `ALLOWED_HOSTS`

2. **Database**
   - Switch to PostgreSQL/MySQL for production
   - Configure database credentials

3. **Static Files**
   - Run `python manage.py collectstatic`
   - Configure static file serving (nginx/Apache)

4. **Media Files**
   - Configure media file storage (S3/CDN)
   - Set proper file upload limits

## 📝 License

This project is created as the Internship Task by Mindriser Institute and Technology.

## 👥 Contributors

- Ranish Bhattarai

## 🤝 Support

For issues or questions, please open an issue on the repository.
