# Endirimall

A discount aggregator platform built with Django.

## Features
- Browse discounted products organized by categories and stores
- Smart search (product, store, category) with real-time results
- Slider for store promotional images
- User authentication (login, registration, profile, logout)
- Multi-language support (Azerbaijani, English, Russian)
- Email subscription form
- Favorite products
- Admin panel for products, categories, slider, discounts, and stores
- SEO: sitemap.xml and robots.txt

## Tech
- Django 5, Bootstrap 5
- PostgreSQL (fallback to SQLite for local dev)

## Quickstart
1. Create and activate a virtualenv
2. Install requirements
3. Set environment variables (or copy `.env.example`)
4. Run migrations and create a superuser
5. Run the server

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export POSTGRES_DB=... POSTGRES_USER=... POSTGRES_PASSWORD=... POSTGRES_HOST=localhost POSTGRES_PORT=5432
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

For i18n compile:
```bash
django-admin makemessages -l az -l ru -l en
django-admin compilemessages
```

## Environment
- `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS`
- PostgreSQL: `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`, `POSTGRES_PORT`

## Notes
- Static files are in `static/`, media uploads in `media/`.
- Slider images upload path: `media/slider/`.