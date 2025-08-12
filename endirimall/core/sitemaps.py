from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from deals.models import Product, Category


class ProductSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return Product.objects.filter(is_active=True)

    def lastmod(self, obj: Product):
        return obj.updated_at or obj.created_at

    def location(self, obj: Product):
        return obj.get_absolute_url()


class CategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return Category.objects.all()

    def location(self, obj: Category):
        return obj.get_absolute_url()