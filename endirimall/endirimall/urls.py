"""
URL configuration for endirimall project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView
from django.http import HttpResponse

# Import sitemaps
from deals.sitemaps import ProductSitemap, CategorySitemap, StoreSitemap

# Define sitemaps
sitemaps = {
    'products': ProductSitemap,
    'categories': CategorySitemap,
    'stores': StoreSitemap,
}

def robots_txt(request):
    """Generate robots.txt file"""
    lines = [
        "User-Agent: *",
        "Allow: /",
        f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")

# Non-i18n URLs (language-independent)
urlpatterns = [
    # SEO URLs
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', robots_txt),
    
    # Language switching
    path('i18n/', include('django.conf.urls.i18n')),
]

# i18n URLs (language-dependent)
urlpatterns += i18n_patterns(
    # Admin
    path('admin/', admin.site.urls),
    
    # Core app (homepage)
    path('', include('core.urls')),
    
    # Deals app
    path('deals/', include('deals.urls')),
    
    # Accounts app
    path('accounts/', include('accounts.urls')),
    
    # Marketing app
    path('marketing/', include('marketing.urls')),
    
    prefix_default_language=False  # Don't add language prefix for default language
)

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Custom admin site configuration
admin.site.site_header = "Endirimall Admin"
admin.site.site_title = "Endirimall Admin Portal"
admin.site.index_title = "Welcome to Endirimall Administration"
