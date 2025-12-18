# Nature Touch — E-Commerce Web Application

**Nature Touch** is a full-stack e-commerce web application built using **Django**, offering a smooth and responsive shopping experience. The platform is designed to showcase products, manage user accounts, handle shopping carts and orders, and process payments — all within a clean, user-friendly interface.

> Developed by **Sabhyata Aryal** and **Soniya Ghimire**.

## Features

- Product listings by categories and subcategories  
- User authentication and account management  
- Add to cart, update quantities, and checkout process  
- Order management for customers and admins  
- Payment integration (khalti sandbox)  
- Email notifications for order confirmations  
- Admin panel for product and order management  
- Media handling for product images  
- Fully responsive design using Bootstrap  



## Tech Stack

| Technology      | Purpose                |
|-----------------|------------------------|
| **Python**      | Backend logic          |
| **Django**      | Web framework          |
| **HTML5**       | Markup language        |
| **CSS3**        | Styling                |
| **Bootstrap 5** | Responsive design      |
| **JavaScript**  | Interactivity          |
| **SQLite**      | Development database   |
| **Khalti**       | Payment gateway        |

---

## Getting Started

### Prerequisites

- Python 3.10 or above  
- pip (Python package manager)  
- virtualenv (optional but recommended)  

---

### Setup Instructions

```bash
# Clone the repo
git clone https://github.com/sabhyata-aryal/E-Commerce-Project.git

# Navigate into the project folder
cd E-Commerce-Project

# (Optional) Create and activate virtual environment
python -m venv env
env\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt

# Apply database migrations
python manage.py migrate

# Create a superuser for admin access
python manage.py createsuperuser

# Start the development server
python manage.py runserver

```
## Admin Panel

Django’s admin panel is available at:
/admin/
Login using the superuser credentials.

## Payments

The project integrates eSewa for payment simulation as well as COD (Cash on Delivery).

## License

You are free to use or modify it — please give credit to the original authors.

## Authors

Sabhyata Aryal https://github.com/sabhyata-aryal
Soniya Ghimire https://github.com/ghimiresonia099
