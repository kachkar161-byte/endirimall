from django.core.management.base import BaseCommand
from django.utils.text import slugify
from deals.models import Store, Category, Product, SliderImage
from decimal import Decimal
import random


class Command(BaseCommand):
    help = 'Populate database with demo data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting demo data population...'))
        
        # Create stores
        stores_data = [
            {'name': 'TechMart', 'website_url': 'https://techmart.az', 'description': 'Electronics and gadgets store'},
            {'name': 'FashionHub', 'website_url': 'https://fashionhub.az', 'description': 'Fashion and clothing store'},
            {'name': 'HomeDecor', 'website_url': 'https://homedecor.az', 'description': 'Home decoration and furniture'},
            {'name': 'SportZone', 'website_url': 'https://sportzone.az', 'description': 'Sports equipment and apparel'},
            {'name': 'BookWorld', 'website_url': 'https://bookworld.az', 'description': 'Books and educational materials'},
        ]
        
        stores = []
        for store_data in stores_data:
            store, created = Store.objects.get_or_create(
                name=store_data['name'],
                defaults={
                    'slug': slugify(store_data['name']),
                    'website_url': store_data['website_url'],
                    'description': store_data['description'],
                    'is_active': True
                }
            )
            stores.append(store)
            if created:
                self.stdout.write(f'Created store: {store.name}')

        # Create categories
        categories_data = [
            {'name': 'Electronics', 'icon': 'laptop', 'description': 'Electronic devices and gadgets'},
            {'name': 'Fashion', 'icon': 'bag', 'description': 'Clothing and accessories'},
            {'name': 'Home & Garden', 'icon': 'house', 'description': 'Home decoration and garden items'},
            {'name': 'Sports', 'icon': 'trophy', 'description': 'Sports equipment and fitness gear'},
            {'name': 'Books', 'icon': 'book', 'description': 'Books and educational materials'},
            {'name': 'Beauty', 'icon': 'heart', 'description': 'Beauty and personal care products'},
            {'name': 'Automotive', 'icon': 'car-front', 'description': 'Car accessories and parts'},
            {'name': 'Toys', 'icon': 'puzzle', 'description': 'Toys and games for children'},
        ]
        
        categories = []
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'slug': slugify(cat_data['name']),
                    'icon': cat_data['icon'],
                    'description': cat_data['description'],
                    'is_active': True
                }
            )
            categories.append(category)
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Create products
        products_data = [
            # Electronics
            {'title': 'iPhone 15 Pro Max', 'description': 'Latest Apple smartphone with advanced features', 'original_price': 1299.99, 'discounted_price': 1199.99, 'category': 'Electronics', 'store': 'TechMart'},
            {'title': 'Samsung Galaxy S24 Ultra', 'description': 'Flagship Android smartphone with S Pen', 'original_price': 1199.99, 'discounted_price': 1099.99, 'category': 'Electronics', 'store': 'TechMart'},
            {'title': 'MacBook Air M3', 'description': 'Lightweight laptop with M3 chip', 'original_price': 1499.99, 'discounted_price': 1399.99, 'category': 'Electronics', 'store': 'TechMart'},
            {'title': 'Sony WH-1000XM5 Headphones', 'description': 'Noise-canceling wireless headphones', 'original_price': 399.99, 'discounted_price': 299.99, 'category': 'Electronics', 'store': 'TechMart'},
            
            # Fashion
            {'title': 'Nike Air Jordan Sneakers', 'description': 'Classic basketball sneakers', 'original_price': 179.99, 'discounted_price': 149.99, 'category': 'Fashion', 'store': 'FashionHub'},
            {'title': 'Levi\'s 501 Jeans', 'description': 'Classic straight-fit jeans', 'original_price': 89.99, 'discounted_price': 69.99, 'category': 'Fashion', 'store': 'FashionHub'},
            {'title': 'Adidas Ultraboost 23', 'description': 'Running shoes with boost technology', 'original_price': 199.99, 'discounted_price': 159.99, 'category': 'Fashion', 'store': 'FashionHub'},
            
            # Home & Garden
            {'title': 'IKEA Sofa Set', 'description': 'Comfortable 3-seater sofa', 'original_price': 799.99, 'discounted_price': 649.99, 'category': 'Home & Garden', 'store': 'HomeDecor'},
            {'title': 'Philips Smart LED Bulbs', 'description': 'Color-changing smart bulbs pack of 4', 'original_price': 79.99, 'discounted_price': 59.99, 'category': 'Home & Garden', 'store': 'HomeDecor'},
            
            # Sports
            {'title': 'Yoga Mat Premium', 'description': 'Non-slip exercise yoga mat', 'original_price': 49.99, 'discounted_price': 34.99, 'category': 'Sports', 'store': 'SportZone'},
            {'title': 'Dumbbells Set 20kg', 'description': 'Adjustable dumbbells for home gym', 'original_price': 199.99, 'discounted_price': 149.99, 'category': 'Sports', 'store': 'SportZone'},
            
            # Books
            {'title': 'Python Programming Book', 'description': 'Complete guide to Python programming', 'original_price': 59.99, 'discounted_price': 39.99, 'category': 'Books', 'store': 'BookWorld'},
            {'title': 'Django Web Development', 'description': 'Learn Django framework step by step', 'original_price': 49.99, 'discounted_price': 34.99, 'category': 'Books', 'store': 'BookWorld'},
        ]
        
        products = []
        for prod_data in products_data:
            # Find category and store
            category = next((cat for cat in categories if cat.name == prod_data['category']), categories[0])
            store = next((st for st in stores if st.name == prod_data['store']), stores[0])
            
            product, created = Product.objects.get_or_create(
                title=prod_data['title'],
                defaults={
                    'slug': slugify(prod_data['title']),
                    'description': prod_data['description'],
                    'original_price': Decimal(str(prod_data['original_price'])),
                    'discounted_price': Decimal(str(prod_data['discounted_price'])),
                    'category': category,
                    'store': store,
                    'deal_url': f"https://{store.name.lower()}.com/deals/{slugify(prod_data['title'])}",
                    'is_active': True,
                    'is_featured': random.choice([True, False])
                }
            )
            products.append(product)
            if created:
                self.stdout.write(f'Created product: {product.title}')

        # Create slider images
        slider_data = [
            {'title': 'Welcome to Endirimall', 'alt_text': 'Welcome banner'},
            {'title': 'Best Electronics Deals', 'alt_text': 'Electronics deals banner'},
            {'title': 'Fashion Sale 50% Off', 'alt_text': 'Fashion sale banner'},
            {'title': 'Home Decor Special Offers', 'alt_text': 'Home decor banner'},
        ]
        
        for i, slide_data in enumerate(slider_data):
            slider, created = SliderImage.objects.get_or_create(
                title=slide_data['title'],
                defaults={
                    'alt_text': slide_data['alt_text'],
                    'order': i,
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(f'Created slider: {slider.title}')

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully populated demo data:\n'
                f'- {len(stores)} stores\n'
                f'- {len(categories)} categories\n'
                f'- {len(products)} products\n'
                f'- {len(slider_data)} slider images'
            )
        )