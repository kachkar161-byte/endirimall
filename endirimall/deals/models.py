from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from PIL import Image


class Store(models.Model):
    """Model for stores/retailers"""
    name = models.CharField(_('Store Name'), max_length=100)
    slug = models.SlugField(_('Slug'), unique=True)
    logo = models.ImageField(_('Logo'), upload_to='stores/', blank=True, null=True)
    website_url = models.URLField(_('Website URL'), blank=True)
    description = models.TextField(_('Description'), blank=True)
    is_active = models.BooleanField(_('Is Active'), default=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    class Meta:
        verbose_name = _('Store')
        verbose_name_plural = _('Stores')
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('deals:store_detail', kwargs={'slug': self.slug})


class Category(models.Model):
    """Model for product categories"""
    name = models.CharField(_('Category Name'), max_length=100)
    slug = models.SlugField(_('Slug'), unique=True)
    icon = models.CharField(_('Icon Class'), max_length=50, blank=True, 
                           help_text=_('Bootstrap icon class (e.g., bi-laptop)'))
    description = models.TextField(_('Description'), blank=True)
    is_active = models.BooleanField(_('Is Active'), default=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('deals:category_detail', kwargs={'slug': self.slug})

    def get_products_count(self):
        return self.products.filter(is_active=True).count()


class Product(models.Model):
    """Model for products/deals"""
    title = models.CharField(_('Product Title'), max_length=200)
    slug = models.SlugField(_('Slug'), unique=True)
    description = models.TextField(_('Description'))
    image = models.ImageField(_('Product Image'), upload_to='products/')
    original_price = models.DecimalField(_('Original Price'), max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(_('Discounted Price'), max_digits=10, decimal_places=2)
    discount_percentage = models.PositiveIntegerField(_('Discount Percentage'), default=0)
    
    # Relationships
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='products', verbose_name=_('Store'))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name=_('Category'))
    
    # Deal information
    deal_url = models.URLField(_('Deal URL'), help_text=_('Link to the actual deal'))
    valid_until = models.DateTimeField(_('Valid Until'), blank=True, null=True)
    
    # Status fields
    is_active = models.BooleanField(_('Is Active'), default=True)
    is_featured = models.BooleanField(_('Is Featured'), default=False)
    
    # Timestamps
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('deals:product_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        # Calculate discount percentage automatically
        if self.original_price and self.discounted_price:
            discount = ((self.original_price - self.discounted_price) / self.original_price) * 100
            self.discount_percentage = round(discount)
        
        super().save(*args, **kwargs)
        
        # Resize image if too large
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 600 or img.width > 600:
                img.thumbnail((600, 600))
                img.save(self.image.path)

    def get_savings(self):
        """Calculate savings amount"""
        return self.original_price - self.discounted_price

    def is_deal_expired(self):
        """Check if deal is expired"""
        if self.valid_until:
            from django.utils import timezone
            return timezone.now() > self.valid_until
        return False


class SliderImage(models.Model):
    """Model for homepage slider images"""
    title = models.CharField(_('Title'), max_length=100)
    image = models.ImageField(_('Slider Image'), upload_to='slider/')
    link_url = models.URLField(_('Link URL'), blank=True, help_text=_('URL to redirect when clicked'))
    alt_text = models.CharField(_('Alt Text'), max_length=200, help_text=_('Alternative text for accessibility'))
    order = models.PositiveIntegerField(_('Display Order'), default=0)
    is_active = models.BooleanField(_('Is Active'), default=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)

    class Meta:
        verbose_name = _('Slider Image')
        verbose_name_plural = _('Slider Images')
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Resize slider image to standard size
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 400 or img.width > 1200:
                img.thumbnail((1200, 400))
                img.save(self.image.path)


class Favorite(models.Model):
    """Model for user favorites"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites', verbose_name=_('User'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorites', verbose_name=_('Product'))
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)

    class Meta:
        verbose_name = _('Favorite')
        verbose_name_plural = _('Favorites')
        unique_together = ('user', 'product')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.product.title}"
