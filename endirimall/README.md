# Endirimall - Discount Aggregator Platform

Endirimall is a comprehensive discount aggregator platform built with Django, designed to help users discover the best deals and discounts from various stores in Azerbaijan.

## 🌟 Features

### Core Functionality
- **Product Browsing**: Browse discounted products organized by categories
- **Smart Search**: Search by product name, store, or category
- **User Authentication**: Complete user registration, login, and profile management
- **Favorites System**: Save and manage favorite products
- **Multi-language Support**: Azerbaijani, English, and Russian languages
- **Responsive Design**: Mobile-friendly interface built with Bootstrap 5

### Advanced Features
- **Slider System**: Promotional image carousel for stores
- **Email Subscriptions**: Newsletter subscription system
- **Admin Panel**: Comprehensive admin interface for managing all content
- **SEO Optimized**: Sitemap, robots.txt, and meta tags
- **Real-time Search**: JavaScript-powered search functionality

## 🚀 Technology Stack

- **Backend**: Django 4.2.7
- **Database**: PostgreSQL
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Icons**: Bootstrap Icons
- **Forms**: Django Crispy Forms
- **Image Processing**: Pillow
- **Deployment**: Gunicorn, WhiteNoise

## 📁 Project Structure

```
endirimall/
├── accounts/          # User authentication and profiles
├── core/             # Main pages and core functionality
├── deals/            # Products, categories, and deals
├── marketing/        # Newsletter and promotional content
├── static/           # CSS, JavaScript, and images
├── media/            # User-uploaded files
├── templates/        # HTML templates
├── locale/           # Translation files
└── manage.py         # Django management script
```

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- PostgreSQL
- pip

### Setup Steps

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

4. **Database setup**
   ```bash
   # Create PostgreSQL database
   createdb endirimall_db
   
   # Run migrations
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

## 🌐 Configuration

### Environment Variables
Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=postgresql://user:password@localhost:5432/endirimall_db
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Database Configuration
Update `settings.py` with your database credentials:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'endirimall_db',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 📱 Usage

### For Users
1. **Browse Products**: Visit the homepage to see featured products and categories
2. **Search**: Use the search bar to find specific products or deals
3. **Create Account**: Register to save favorites and manage preferences
4. **Save Favorites**: Click the heart icon to save products to your favorites
5. **Language Switch**: Use the language switcher in the navigation

### For Administrators
1. **Access Admin Panel**: Visit `/admin/` and login with superuser credentials
2. **Manage Content**: Add/edit products, categories, stores, and slider images
3. **User Management**: Monitor user accounts and activities
4. **Analytics**: View product views and user statistics

## 🌍 Internationalization

The platform supports three languages:
- **Azerbaijani (az)**: Default language
- **English (en)**: International users
- **Russian (ru)**: Russian-speaking users

### Adding New Languages
1. Add language to `LANGUAGES` in `settings.py`
2. Create translation files using `django-admin makemessages -l <language_code>`
3. Translate the `.po` files
4. Compile messages with `django-admin compilemessages`

## 🔧 Customization

### Adding New Features
1. Create new Django apps for additional functionality
2. Add models, views, and templates
3. Update URL patterns
4. Include in main settings

### Styling
- Modify `static/css/style.css` for custom styles
- Update Bootstrap variables in CSS
- Add custom JavaScript in `static/js/main.js`

## 📊 Database Models

### Core Models
- **User**: Extended user model with profile information
- **Product**: Product details, pricing, and images
- **Category**: Product categorization system
- **Store**: Store information and branding
- **Favorite**: User favorite products
- **SliderImage**: Promotional carousel images

### Marketing Models
- **EmailSubscription**: Newsletter subscribers
- **Newsletter**: Email campaign management
- **PromotionalBanner**: Marketing banners

## 🚀 Deployment

### Production Settings
1. Set `DEBUG = False`
2. Configure production database
3. Set up static file serving
4. Configure email backend
5. Set secure `SECRET_KEY`

### Recommended Stack
- **Web Server**: Nginx
- **Application Server**: Gunicorn
- **Database**: PostgreSQL
- **Static Files**: WhiteNoise or CDN
- **Media Files**: Cloud storage (AWS S3, etc.)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

## 🔮 Future Enhancements

- **Mobile App**: Native mobile applications
- **API**: RESTful API for third-party integrations
- **Analytics**: Advanced user behavior tracking
- **Notifications**: Push notifications for deals
- **Social Features**: User reviews and ratings
- **Price Tracking**: Historical price monitoring

## 📈 Performance Optimization

- Database query optimization
- Image compression and lazy loading
- Caching strategies
- CDN integration
- Database indexing

---

**Endirimall** - Making deals accessible to everyone! 🎉