from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _
from deals.models import Product, SliderImage, Category


class HomeView(TemplateView):
    """Homepage view displaying featured products and slider"""
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get featured products
        context['featured_products'] = Product.objects.filter(
            is_active=True, 
            is_featured=True
        ).select_related('store', 'category')[:8]
        
        # Get latest products
        context['latest_products'] = Product.objects.filter(
            is_active=True
        ).select_related('store', 'category').order_by('-created_at')[:12]
        
        # Get slider images
        context['slider_images'] = SliderImage.objects.filter(
            is_active=True
        ).order_by('order')[:5]
        
        # Get categories for navigation
        context['categories'] = Category.objects.filter(
            is_active=True
        ).order_by('name')[:8]
        
        # Page metadata
        context['page_title'] = _('Best Deals and Discounts')
        context['page_description'] = _(
            'Discover the best deals and discounts from top stores. '
            'Save money on electronics, fashion, home goods and more.'
        )
        
        return context
