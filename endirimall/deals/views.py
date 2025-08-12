from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.urls import reverse_lazy

from .models import Product, Category, Store, Favorite


class ProductListView(ListView):
    """View for listing all products"""
    model = Product
    template_name = 'deals/product_list.html'
    context_object_name = 'products'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True).select_related('store', 'category')
        
        # Filter by category
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        # Filter by store
        store_slug = self.request.GET.get('store')
        if store_slug:
            queryset = queryset.filter(store__slug=store_slug)
        
        # Sort options
        sort = self.request.GET.get('sort', 'newest')
        if sort == 'price_low':
            queryset = queryset.order_by('discounted_price')
        elif sort == 'price_high':
            queryset = queryset.order_by('-discounted_price')
        elif sort == 'discount':
            queryset = queryset.order_by('-discount_percentage')
        else:  # newest
            queryset = queryset.order_by('-created_at')
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_active=True)
        context['stores'] = Store.objects.filter(is_active=True)
        context['current_category'] = self.request.GET.get('category', '')
        context['current_store'] = self.request.GET.get('store', '')
        context['current_sort'] = self.request.GET.get('sort', 'newest')
        return context


class ProductDetailView(DetailView):
    """View for product details"""
    model = Product
    template_name = 'deals/product_detail.html'
    context_object_name = 'product'
    slug_field = 'slug'
    
    def get_queryset(self):
        return Product.objects.filter(is_active=True).select_related('store', 'category')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Check if user has favorited this product
        if self.request.user.is_authenticated:
            context['is_favorited'] = Favorite.objects.filter(
                user=self.request.user, 
                product=self.object
            ).exists()
        else:
            context['is_favorited'] = False
        
        # Get related products from same category
        context['related_products'] = Product.objects.filter(
            category=self.object.category,
            is_active=True
        ).exclude(id=self.object.id).select_related('store', 'category')[:4]
        
        return context


class FeaturedProductsView(ListView):
    """View for featured products"""
    model = Product
    template_name = 'deals/featured_products.html'
    context_object_name = 'products'
    paginate_by = 16
    
    def get_queryset(self):
        return Product.objects.filter(
            is_active=True, 
            is_featured=True
        ).select_related('store', 'category').order_by('-created_at')


class CategoryListView(ListView):
    """View for listing all categories"""
    model = Category
    template_name = 'deals/category_list.html'
    context_object_name = 'categories'
    
    def get_queryset(self):
        return Category.objects.filter(is_active=True).order_by('name')


class CategoryDetailView(DetailView):
    """View for category details with products"""
    model = Category
    template_name = 'deals/category_detail.html'
    context_object_name = 'category'
    slug_field = 'slug'
    
    def get_queryset(self):
        return Category.objects.filter(is_active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get products in this category
        products = Product.objects.filter(
            category=self.object,
            is_active=True
        ).select_related('store', 'category').order_by('-created_at')
        
        # Paginate products
        paginator = Paginator(products, 12)
        page_number = self.request.GET.get('page')
        context['products'] = paginator.get_page(page_number)
        
        return context


class StoreListView(ListView):
    """View for listing all stores"""
    model = Store
    template_name = 'deals/store_list.html'
    context_object_name = 'stores'
    
    def get_queryset(self):
        return Store.objects.filter(is_active=True).order_by('name')


class StoreDetailView(DetailView):
    """View for store details with products"""
    model = Store
    template_name = 'deals/store_detail.html'
    context_object_name = 'store'
    slug_field = 'slug'
    
    def get_queryset(self):
        return Store.objects.filter(is_active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get products from this store
        products = Product.objects.filter(
            store=self.object,
            is_active=True
        ).select_related('store', 'category').order_by('-created_at')
        
        # Paginate products
        paginator = Paginator(products, 12)
        page_number = self.request.GET.get('page')
        context['products'] = paginator.get_page(page_number)
        
        return context


class SearchView(TemplateView):
    """View for search results"""
    template_name = 'deals/search_results.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', '').strip()
        
        if query:
            # Search in products, stores, and categories
            products = Product.objects.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(store__name__icontains=query) |
                Q(category__name__icontains=query),
                is_active=True
            ).select_related('store', 'category').distinct()
            
            # Paginate results
            paginator = Paginator(products, 12)
            page_number = self.request.GET.get('page')
            context['products'] = paginator.get_page(page_number)
        else:
            context['products'] = None
        
        context['query'] = query
        return context


class SearchAPIView(View):
    """API view for real-time search suggestions"""
    
    def get(self, request):
        query = request.GET.get('q', '').strip()
        results = []
        
        if query and len(query) >= 2:
            # Search products
            products = Product.objects.filter(
                Q(title__icontains=query),
                is_active=True
            ).select_related('store', 'category')[:5]
            
            for product in products:
                results.append({
                    'type': 'product',
                    'title': product.title,
                    'url': product.get_absolute_url(),
                    'image': product.image.url if product.image else '',
                    'price': str(product.discounted_price),
                    'store': product.store.name,
                })
            
            # Search stores
            stores = Store.objects.filter(
                name__icontains=query,
                is_active=True
            )[:3]
            
            for store in stores:
                results.append({
                    'type': 'store',
                    'title': store.name,
                    'url': store.get_absolute_url(),
                    'image': store.logo.url if store.logo else '',
                })
            
            # Search categories
            categories = Category.objects.filter(
                name__icontains=query,
                is_active=True
            )[:3]
            
            for category in categories:
                results.append({
                    'type': 'category',
                    'title': category.name,
                    'url': category.get_absolute_url(),
                    'icon': category.icon,
                })
        
        return JsonResponse({'results': results})


class FavoritesView(LoginRequiredMixin, TemplateView):
    """View for user's favorite products"""
    template_name = 'deals/favorites.html'
    login_url = reverse_lazy('accounts:login')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        favorites = Favorite.objects.filter(
            user=self.request.user
        ).select_related('product__store', 'product__category')
        
        # Paginate favorites
        paginator = Paginator(favorites, 12)
        page_number = self.request.GET.get('page')
        context['favorites'] = paginator.get_page(page_number)
        
        return context


class ToggleFavoriteView(LoginRequiredMixin, View):
    """API view for toggling product favorites"""
    
    def post(self, request, product_id):
        try:
            product = get_object_or_404(Product, id=product_id, is_active=True)
            favorite, created = Favorite.objects.get_or_create(
                user=request.user,
                product=product
            )
            
            if not created:
                favorite.delete()
                is_favorited = False
                message = _('Removed from favorites')
            else:
                is_favorited = True
                message = _('Added to favorites')
            
            return JsonResponse({
                'success': True,
                'is_favorited': is_favorited,
                'message': str(message)
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(_('An error occurred'))
            }, status=400)
