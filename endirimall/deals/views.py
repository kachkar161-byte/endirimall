"""
Deals app views for products, categories, search, and favorites.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

from .models import Product, Category, Store, Favorite, SliderImage
from .forms import ProductSearchForm


def product_list(request):
    """
    Display a list of all active products with pagination.
    """
    products = Product.objects.filter(is_active=True).select_related('category', 'store')
    
    # Filtering
    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)
    
    store_slug = request.GET.get('store')
    if store_slug:
        products = products.filter(store__slug=store_slug)
    
    # Sorting
    sort_by = request.GET.get('sort', 'newest')
    if sort_by == 'price_low':
        products = products.order_by('discounted_price')
    elif sort_by == 'price_high':
        products = products.order_by('-discounted_price')
    elif sort_by == 'discount':
        products = products.order_by('-discount_percentage')
    else:  # newest
        products = products.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get categories for filter sidebar
    categories = Category.objects.filter(is_active=True)
    stores = Store.objects.filter(is_active=True)
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'stores': stores,
        'current_category': category_slug,
        'current_store': store_slug,
        'current_sort': sort_by,
        'page_title': _('Bütün Endirimlər'),
    }
    
    return render(request, 'deals/product_list.html', context)


def product_detail(request, slug):
    """
    Display detailed information about a specific product.
    """
    product = get_object_or_404(Product, slug=slug, is_active=True)
    
    # Track view
    if request.user.is_authenticated:
        ProductView.objects.create(
            product=product,
            ip_address=request.META.get('REMOTE_ADDR', ''),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
    
    # Check if product is in user's favorites
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, product=product).exists()
    
    # Get related products
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'is_favorite': is_favorite,
        'related_products': related_products,
        'page_title': product.name,
    }
    
    return render(request, 'deals/product_detail.html', context)


def category_detail(request, slug):
    """
    Display products from a specific category.
    """
    category = get_object_or_404(Category, slug=slug, is_active=True)
    products = Product.objects.filter(
        category=category,
        is_active=True
    ).select_related('store').order_by('-created_at')
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get subcategories
    subcategories = category.children.filter(is_active=True)
    
    context = {
        'category': category,
        'page_obj': page_obj,
        'subcategories': subcategories,
        'page_title': f"{category.name} - Endirimlər",
    }
    
    return render(request, 'deals/category_detail.html', context)


def store_detail(request, slug):
    """
    Display products from a specific store.
    """
    store = get_object_or_404(Store, slug=slug, is_active=True)
    products = Product.objects.filter(
        store=store,
        is_active=True
    ).select_related('category').order_by('-created_at')
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'store': store,
        'page_obj': page_obj,
        'page_title': f"{store.name} - Endirimlər",
    }
    
    return render(request, 'deals/store_detail.html', context)


def search_products(request):
    """
    Search products by name, store, or category.
    """
    query = request.GET.get('q', '')
    products = []
    
    if query:
        # Search in product name, description, store name, and category name
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(store__name__icontains=query) |
            Q(category__name__icontains=query),
            is_active=True
        ).select_related('category', 'store').order_by('-created_at')
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'query': query,
        'page_obj': page_obj,
        'page_title': f'Axtarış: {query}' if query else _('Məhsul Axtarışı'),
    }
    
    return render(request, 'deals/search_results.html', context)


@login_required
def favorite_list(request):
    """
    Display user's favorite products.
    """
    favorites = Favorite.objects.filter(user=request.user).select_related('product', 'product__category', 'product__store')
    
    # Pagination
    paginator = Paginator(favorites, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'page_title': _('Sevimli Məhsullar'),
    }
    
    return render(request, 'deals/favorite_list.html', context)


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def toggle_favorite(request):
    """
    Toggle favorite status for a product via AJAX.
    """
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        
        if not product_id:
            return JsonResponse({'success': False, 'message': _('Məhsul ID tələb olunur')})
        
        product = get_object_or_404(Product, id=product_id, is_active=True)
        favorite, created = Favorite.objects.get_or_create(
            user=request.user,
            product=product
        )
        
        if not created:
            # Remove from favorites
            favorite.delete()
            is_favorite = False
            message = _('Məhsul sevimlilərdən silindi')
        else:
            is_favorite = True
            message = _('Məhsul sevimlilərə əlavə edildi')
        
        return JsonResponse({
            'success': True,
            'is_favorite': is_favorite,
            'message': message
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': _('Xəta baş verdi')})
    except Exception as e:
        return JsonResponse({'success': False, 'message': _('Xəta baş verdi')})


def hot_deals(request):
    """
    Display hot deals (products with high discounts).
    """
    products = Product.objects.filter(
        is_active=True,
        is_hot_deal=True
    ).select_related('category', 'store').order_by('-discount_percentage')
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'page_title': _('Hot Deals - Ən Böyük Endirimlər'),
    }
    
    return render(request, 'deals/hot_deals.html', context)


def featured_products(request):
    """
    Display featured products.
    """
    products = Product.objects.filter(
        is_active=True,
        is_featured=True
    ).select_related('category', 'store').order_by('-created_at')
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'page_title': _('Seçilmiş Məhsullar'),
    }
    
    return render(request, 'deals/featured_products.html', context)