"""
Core views for endirimall project.
"""
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

from deals.models import Product, Category, SliderImage
from marketing.models import EmailSubscription


def home(request):
    """
    Homepage view displaying featured products, categories, and slider.
    """
    # Get featured products
    featured_products = Product.objects.filter(is_featured=True)[:8]
    
    # Get all categories
    categories = Category.objects.all()[:6]
    
    # Get slider images
    slider_images = SliderImage.objects.filter(is_active=True).order_by('order')
    
    context = {
        'featured_products': featured_products,
        'categories': categories,
        'slider_images': slider_images,
        'page_title': _('Endirimall - Ən yaxşı endirimlər'),
    }
    
    return render(request, 'core/home.html', context)


def about(request):
    """
    About page view.
    """
    context = {
        'page_title': _('Haqqımızda'),
    }
    return render(request, 'core/about.html', context)


def contact(request):
    """
    Contact page view.
    """
    context = {
        'page_title': _('Əlaqə'),
    }
    return render(request, 'core/contact.html', context)


def privacy_policy(request):
    """
    Privacy policy page view.
    """
    context = {
        'page_title': _('Gizlilik Siyasəti'),
    }
    return render(request, 'core/privacy_policy.html', context)


def terms_of_service(request):
    """
    Terms of service page view.
    """
    context = {
        'page_title': _('İstifadə Şərtləri'),
    }
    return render(request, 'core/terms_of_service.html', context)


@csrf_exempt
@require_http_methods(["POST"])
def newsletter_subscription(request):
    """
    Handle newsletter subscription via AJAX.
    """
    try:
        data = json.loads(request.body)
        email = data.get('email')
        
        if not email:
            return JsonResponse({'success': False, 'message': _('Email ünvanı tələb olunur')})
        
        # Check if email already exists
        if EmailSubscription.objects.filter(email=email).exists():
            return JsonResponse({'success': False, 'message': _('Bu email artıq abunədir')})
        
        # Create new subscription
        EmailSubscription.objects.create(email=email)
        
        messages.success(request, _('Uğurla abunə oldunuz!'))
        return JsonResponse({'success': True, 'message': _('Uğurla abunə oldunuz!')})
        
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': _('Xəta baş verdi')})
    except Exception as e:
        return JsonResponse({'success': False, 'message': _('Xəta baş verdi')})


def sitemap_xml(request):
    """
    Generate sitemap.xml for SEO.
    """
    from django.contrib.sitemaps import Sitemap
    from django.http import HttpResponse
    from django.template.loader import render_to_string
    
    # Get all products and categories
    products = Product.objects.all()
    categories = Category.objects.all()
    
    context = {
        'products': products,
        'categories': categories,
        'domain': request.get_host(),
    }
    
    xml = render_to_string('core/sitemap.xml', context)
    return HttpResponse(xml, content_type='application/xml')


def robots_txt(request):
    """
    Generate robots.txt for SEO.
    """
    from django.http import HttpResponse
    
    robots_content = """User-agent: *
Allow: /
Disallow: /admin/
Disallow: /accounts/
Disallow: /media/

Sitemap: https://{}/sitemap.xml
""".format(request.get_host())
    
    return HttpResponse(robots_content, content_type='text/plain')