from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from django.utils.translation import gettext as _

from .models import Product, SliderImage, Favorite, Category, Store


def product_list(request):
    """List all active products with optional category/store filters."""
    products = Product.objects.filter(is_active=True)
    category_slug = request.GET.get('category')
    store_slug = request.GET.get('store')

    if category_slug:
        products = products.filter(category__slug=category_slug)
    if store_slug:
        products = products.filter(store__slug=store_slug)

    context = {
        'products': products,
        'slider_images': SliderImage.objects.all(),
        'categories': Category.objects.all(),
        'stores': Store.objects.all(),
    }
    return render(request, 'core/home.html', context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, is_active=True)
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, product=product).exists()
    context = {
        'product': product,
        'is_favorite': is_favorite,
    }
    return render(request, 'deals/product_detail.html', context)


@login_required
def toggle_favorite(request):
    if request.method != 'POST' or not request.is_ajax():
        return HttpResponseBadRequest()

    product_id = request.POST.get('product_id')
    product = get_object_or_404(Product, id=product_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)

    if not created:
        favorite.delete()
        status = 'removed'
    else:
        status = 'added'
    return JsonResponse({'status': status})


def search_products(request):
    """Return JSON list of products for smart search autocomplete."""
    query = request.GET.get('q', '').strip()
    results = []
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(store__name__icontains=query) | Q(category__name__icontains=query),
            is_active=True
        )[:10]
        for product in products:
            results.append({
                'id': product.id,
                'name': product.name,
                'store': product.store.name,
                'category': product.category.name,
                'image': product.image.url if product.image else '',
                'url': product.get_absolute_url() if hasattr(product, 'get_absolute_url') else '',
            })
    return JsonResponse({'results': results})
