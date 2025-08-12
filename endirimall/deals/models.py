"""
Deals app models for products, categories, stores, and favorites.
"""
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid


class Store(models.Model):
    """
    Store model for managing different stores.
    """
    name = models.CharField(_('Store Name'), max_length=200)
    slug = models.SlugField(_('Slug'), max_length=200, unique=True)
    description = models.TextField(_('Description'), blank=True)
    logo = models.ImageField(_('Logo'), upload_to='stores/logos/', blank=True, null=True)
    website = models.URLField(_('Website'), blank=True)
    phone = models.CharField(_('Phone'), max_length=20, blank=True)
    address = models.TextField(_('Address'), blank=True)
    is_active = models.BooleanField(_('Active'), default=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    
    class Meta:
        verbose_name = _('Store')
        verbose_name_plural = _('Stores')
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('deals:store_detail', args=[self.slug])


class Category(models.Model):
    """
    Category model for organizing products.
    """
    name = models.CharField(_('Category Name'), max_length=200)
    slug = models.SlugField(_('Slug'), max_length=200, unique=True)
    description = models.TextField(_('Description'), blank=True)
    image = models.ImageField(_('Image'), upload_to='categories/', blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, 
                              related_name='children', verbose_name=_('Parent Category'))
    is_active = models.BooleanField(_('Active'), default=True)
    order = models.PositiveIntegerField(_('Order'), default=0)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    
    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('deals:category_detail', args=[self.slug])
    
    def get_products_count(self):
        """Get the count of products in this category."""
        return self.product_set.filter(is_active=True).count()


class Product(models.Model):
    """
    Product model for managing discounted products.
    """
    name = models.CharField(_('Product Name'), max_length=300)
    slug = models.SlugField(_('Slug'), max_length=300, unique=True)
    description = models.TextField(_('Description'), blank=True)
    short_description = models.CharField(_('Short Description'), max_length=500, blank=True)
    
    # Pricing
    original_price = models.DecimalField(_('Original Price'), max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(_('Discounted Price'), max_digits=10, decimal_places=2)
    discount_percentage = models.PositiveIntegerField(_('Discount Percentage'), 
                                                    validators=[MinValueValidator(0), MaxValueValidator(100)])
    
    # Images
    main_image = models.ImageField(_('Main Image'), upload_to='products/main/')
    additional_images = models.JSONField(_('Additional Images'), default=list, blank=True)
    
    # Relationships
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_('Category'))
    store = models.ForeignKey(Store, on_delete=models.CASCADE, verbose_name=_('Store'))
    
    # Status
    is_active = models.BooleanField(_('Active'), default=True)
    is_featured = models.BooleanField(_('Featured'), default=False)
    is_hot_deal = models.BooleanField(_('Hot Deal'), default=False)
    
    # Metadata
    sku = models.CharField(_('SKU'), max_length=100, blank=True)
    brand = models.CharField(_('Brand'), max_length=100, blank=True)
    model = models.CharField(_('Model'), max_length=100, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    expires_at = models.DateTimeField(_('Expires At'), blank=True, null=True)
    
    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['category']),
            models.Index(fields=['store']),
            models.Index(fields=['is_active']),
            models.Index(fields=['is_featured']),
        ]
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        
        # Calculate discount percentage if not provided
        if not self.discount_percentage and self.original_price and self.discounted_price:
            self.discount_percentage = int(((self.original_price - self.discounted_price) / self.original_price) * 100)
        
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('deals:product_detail', args=[self.slug])
    
    def get_savings_amount(self):
        """Calculate the amount saved."""
        return self.original_price - self.discounted_price
    
    def is_expired(self):
        """Check if the deal has expired."""
        if self.expires_at:
            from django.utils import timezone
            return timezone.now() > self.expires_at
        return False


class Favorite(models.Model):
    """
    Favorite model for users to save products.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('User'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('Product'))
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('Favorite')
        verbose_name_plural = _('Favorites')
        unique_together = ['user', 'product']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.product.name}"


class SliderImage(models.Model):
    """
    Slider image model for promotional content.
    """
    title = models.CharField(_('Title'), max_length=200)
    subtitle = models.CharField(_('Subtitle'), max_length=300, blank=True)
    image = models.ImageField(_('Image'), upload_to='slider/')
    link = models.URLField(_('Link'), blank=True)
    button_text = models.CharField(_('Button Text'), max_length=50, blank=True)
    is_active = models.BooleanField(_('Active'), default=True)
    order = models.PositiveIntegerField(_('Order'), default=0)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('Slider Image')
        verbose_name_plural = _('Slider Images')
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return self.title


class ProductView(models.Model):
    """
    Model to track product views for analytics.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('Product'))
    ip_address = models.GenericIPAddressField(_('IP Address'))
    user_agent = models.TextField(_('User Agent'), blank=True)
    viewed_at = models.DateTimeField(_('Viewed At'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('Product View')
        verbose_name_plural = _('Product Views')
        ordering = ['-viewed_at']
    
    def __str__(self):
        return f"{self.product.name} - {self.ip_address}"