#!/bin/bash

# Endirimall Deployment Script
# This script sets up and deploys the Endirimall Django project

set -e  # Exit on any error

echo "🚀 Starting Endirimall deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

print_success "Python 3 is installed"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    print_error "pip3 is not installed. Please install pip3."
    exit 1
fi

print_success "pip3 is installed"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    print_status "Creating virtual environment..."
    python3 -m venv venv
    print_success "Virtual environment created"
else
    print_warning "Virtual environment already exists"
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate
print_success "Virtual environment activated"

# Install requirements
print_status "Installing Python dependencies..."
pip install -r requirements.txt
print_success "Dependencies installed"

# Run migrations
print_status "Running database migrations..."
python manage.py migrate
print_success "Database migrations completed"

# Create superuser if it doesn't exist
print_status "Checking for superuser..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@endirimall.com', 'admin123')
    print('Superuser created: admin/admin123')
else:
    print('Superuser already exists')
"

# Populate demo data
print_status "Populating demo data..."
python manage.py populate_demo_data
print_success "Demo data populated"

# Generate translation files
print_status "Generating translation files..."
if command -v msgfmt &> /dev/null; then
    python manage.py makemessages -l az --ignore=venv
    python manage.py makemessages -l ru --ignore=venv
    python manage.py compilemessages
    print_success "Translation files generated"
else
    print_warning "gettext not installed, skipping translation files"
fi

# Collect static files (for production)
if [ "$1" == "--production" ]; then
    print_status "Collecting static files for production..."
    python manage.py collectstatic --noinput
    print_success "Static files collected"
fi

print_success "🎉 Endirimall deployment completed successfully!"
echo ""
echo "📋 Setup Summary:"
echo "=================="
echo "• Project: Endirimall Discount Aggregator"
echo "• Framework: Django 4.2"
echo "• Database: SQLite (development)"
echo "• Admin User: admin"
echo "• Admin Password: admin123"
echo "• Admin Email: admin@endirimall.com"
echo ""
echo "🌐 Access URLs:"
echo "==============="
echo "• Frontend: http://localhost:8000/"
echo "• Admin Panel: http://localhost:8000/admin/"
echo "• API Search: http://localhost:8000/deals/api/search/"
echo ""
echo "🚀 To start the development server, run:"
echo "   source venv/bin/activate"
echo "   python manage.py runserver"
echo ""
echo "📚 For more information, check the README.md file"
echo ""
print_success "Happy coding! 🎯"