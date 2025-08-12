from django.shortcuts import render
from django.http import HttpResponse
from deals.models import Product, SliderImage


def home(request):
    slider_images = SliderImage.objects.filter(is_active=True).order_by("display_order")[:10]
    latest_products = Product.objects.filter(is_active=True).select_related("store", "category").order_by("-created_at")[:12]
    return render(request, "core/home.html", {"slider_images": slider_images, "latest_products": latest_products})


def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow:",
        "Sitemap: /sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")