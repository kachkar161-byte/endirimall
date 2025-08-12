from django.contrib import admin
from .models import Category, Store, Product, SliderImage, Favorite


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "website")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "store", "category", "original_price", "discounted_price", "is_active")
    list_filter = ("store", "category", "is_active")
    search_fields = ("name", "store__name", "category__name")
    autocomplete_fields = ("store", "category")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(SliderImage)
class SliderImageAdmin(admin.ModelAdmin):
    list_display = ("title", "store", "is_active", "display_order")
    list_filter = ("is_active", "store")


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "created_at")
    autocomplete_fields = ("user", "product")