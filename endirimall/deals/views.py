from __future__ import annotations
from django.db.models import Q, Count
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpRequest, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Product, Category, Store, Favorite


def product_list(request: HttpRequest, slug: str | None = None, **kwargs):
    products = Product.objects.filter(is_active=True).select_related("store", "category")
    categories = Category.objects.all()
    stores = Store.objects.all()

    current_category = None
    current_store = None

    path = request.path
    if path.startswith("/az/") or path.startswith("/en/") or path.startswith("/ru/"):
        # Trim language prefix for matching
        path = "/".join(path.split("/")[2:])
        path = "/" + path if path else "/"

    if path.startswith("/deals/category/") and slug:
        current_category = get_object_or_404(Category, slug=slug)
        products = products.filter(category=current_category)
    elif path.startswith("/deals/store/") and slug:
        current_store = get_object_or_404(Store, slug=slug)
        products = products.filter(store=current_store)

    q = request.GET.get("q", "").strip()
    if q:
        products = products.filter(
            Q(name__icontains=q)
            | Q(description__icontains=q)
            | Q(store__name__icontains=q)
            | Q(category__name__icontains=q)
        )

    favorites = set()
    if request.user.is_authenticated:
        favorites = set(
            Favorite.objects.filter(user=request.user, product__in=products).values_list("product_id", flat=True)
        )

    return render(
        request,
        "deals/product_list.html",
        {
            "products": products,
            "categories": categories,
            "stores": stores,
            "current_category": current_category,
            "current_store": current_store,
            "favorites": favorites,
            "query": q,
        },
    )


def product_detail(request: HttpRequest, store_slug: str, slug: str):
    product = get_object_or_404(
        Product.objects.select_related("store", "category"), store__slug=store_slug, slug=slug, is_active=True
    )

    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, product=product).exists()

    return render(request, "deals/product_detail.html", {"product": product, "is_favorite": is_favorite})


def search(request: HttpRequest):
    q = request.GET.get("q", "").strip()
    if not q:
        return JsonResponse({"results": []})

    products = (
        Product.objects.filter(is_active=True)
        .filter(
            Q(name__icontains=q)
            | Q(description__icontains=q)
            | Q(store__name__icontains=q)
            | Q(category__name__icontains=q)
        )
        .select_related("store", "category")
        .order_by("-created_at")[:10]
    )

    data = [
        {
            "id": p.id,
            "name": p.name,
            "url": p.get_absolute_url(),
            "store": p.store.name,
            "category": p.category.name if p.category else None,
            "image": p.image.url if p.image else None,
            "discount": p.discount_percentage,
            "price": str(p.discounted_price),
        }
        for p in products
    ]
    return JsonResponse({"results": data})


@login_required
def toggle_favorite(request: HttpRequest, product_id: int):
    if request.method != "POST":
        return HttpResponseBadRequest("POST required")

    product = get_object_or_404(Product, id=product_id, is_active=True)
    fav, created = Favorite.objects.get_or_create(user=request.user, product=product)
    if not created:
        fav.delete()
        status = "removed"
    else:
        status = "added"

    count = Favorite.objects.filter(user=request.user).count()
    return JsonResponse({"status": status, "favorite_count": count})