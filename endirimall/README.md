# Endirimall - Discount Aggregator Platform

A comprehensive Django-based discount aggregator platform that helps users find the best deals and discounts from various stores.

## Features

### 🛍️ Core Features
- **Product Listings**: Browse discounted products from multiple stores
- **Smart Search**: Real-time search with suggestions for products, stores, and categories
- **Categories**: Organized product categories with Bootstrap icons
- **Store Pages**: Dedicated pages for each store with their deals
- **Featured Deals**: Highlighted special offers and promotions
- **Favorites System**: Save favorite products (requires login)

### 🌐 Multi-language Support
- **Languages**: English, Azerbaijani (Azərbaycan), Russian (Русский)
- **Language Switcher**: Easy language switching in navigation
- **Internationalization**: Full i18n support with Django's translation system

### 👤 User Management
- **Authentication**: Login, registration, and logout
- **User Profiles**: Extended user profiles with avatars and preferences
- **Password Management**: Password change and reset functionality
- **Favorites**: Personal favorite products list

### 📧 Marketing Features
- **Newsletter Subscription**: Email subscription system
- **Slider**: Homepage promotional slider
- **SEO Optimized**: Meta tags, Open Graph, Twitter Cards
- **Sitemap & Robots.txt**: Search engine optimization

### 📱 Responsive Design
- **Mobile-First**: Fully responsive Bootstrap 5 design
- **Modern UI**: Clean and intuitive user interface
- **Accessibility**: WCAG compliant with proper ARIA labels

### ⚡ Advanced Features
- **Real-time Search**: AJAX-powered search suggestions
- **Image Optimization**: Automatic image resizing
- **Admin Panel**: Comprehensive Django admin interface
- **Performance**: Optimized database queries and caching

## Technology Stack

- **Backend**: Django 4.2
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Database**: SQLite (development) / PostgreSQL (production)
- **Icons**: Bootstrap Icons
- **Languages**: Python 3.8+

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Git

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd endirimall
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Generate translation files (optional)**
   ```bash
   python manage.py makemessages -l az
   python manage.py makemessages -l ru
   python manage.py compilemessages
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Frontend: http://127.0.0.1:8000/
   - Admin Panel: http://127.0.0.1:8000/admin/
   - Default admin credentials: admin/admin123

## Project Structure

```
endirimall/
├── accounts/           # User authentication and profiles
├── core/              # Homepage and shared functionality
├── deals/             # Products, categories, stores, favorites
├── marketing/         # Email subscriptions
├── media/            # User uploaded files
├── static/           # Static files (CSS, JS, images)
├── templates/        # HTML templates
├── locale/           # Translation files
├── endirimall/       # Main project settings
├── manage.py         # Django management script
└── requirements.txt  # Python dependencies
```

## Configuration

### Database Configuration

**For PostgreSQL (Production):**
```python
# In settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'endirimall',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Environment Variables

Create a `.env` file in the project root:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=postgresql://user:password@localhost:5432/endirimall
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

## Admin Panel

The admin panel provides comprehensive management tools:

### Deals Management
- **Products**: Add/edit deals with automatic discount calculation
- **Categories**: Manage product categories with Bootstrap icons
- **Stores**: Store information and branding
- **Slider Images**: Homepage promotional slider
- **Favorites**: Monitor user favorites

### User Management
- **Users**: Extended user management with profiles
- **User Profiles**: Avatar, preferences, and personal information

### Marketing
- **Email Subscriptions**: Newsletter subscriber management
- **Export functionality**: CSV export of subscribers

## API Endpoints

### Search API
- `GET /deals/api/search/?q=query` - Real-time search suggestions

### Favorites API
- `POST /deals/api/toggle-favorite/<product_id>/` - Toggle product favorite

### Newsletter API
- `POST /marketing/api/subscribe/` - Subscribe to newsletter

## Deployment

### Production Settings

1. **Set DEBUG to False**
   ```python
   DEBUG = False
   ALLOWED_HOSTS = ['your-domain.com']
   ```

2. **Configure Static Files**
   ```bash
   python manage.py collectstatic
   ```

3. **Configure Media Files**
   Ensure media files are served properly in production.

4. **Database Migration**
   ```bash
   python manage.py migrate
   ```

### Docker Deployment (Optional)

Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "endirimall.wsgi:application"]
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue in the repository
- Contact: admin@endirimall.com

## Acknowledgments

- Bootstrap team for the amazing CSS framework
- Django community for the excellent web framework
- Bootstrap Icons for the icon set

---

**Made with ❤️ in Azerbaijan**