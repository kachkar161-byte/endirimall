"""
Sitemap configuration for SEO.
"""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from deals.models import Product, Category


class ProductSitemap(Sitemap):
    """
    Sitemap for products.
    """
    changefreq = 'weekly'
    priority = 0.8
    
    def items(self):
        return Product.objects.filter(is_active=True)
    
    def lastmod(self, obj):
        return obj.updated_at
    
    def location(self, obj):
        return reverse('deals:product_detail', args=[obj.slug])


class CategorySitemap(Sitemap):
    """
    Sitemap for categories.
    """
    changefreq = 'monthly'
    priority = 0.6
    
    def items(self):
        return Category.objects.filter(is_active=True)
    
    def lastmod(self, obj):
        return obj.updated_at
    
    def location(self, obj):
        return reverse('deals:category_detail', args=[obj.slug])