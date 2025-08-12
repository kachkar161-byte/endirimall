from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Product, Category, Store


class ProductSitemap(Sitemap):
    """Sitemap for products"""
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return Product.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()


class CategorySitemap(Sitemap):
    """Sitemap for categories"""
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Category.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()


class StoreSitemap(Sitemap):
    """Sitemap for stores"""
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return Store.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()