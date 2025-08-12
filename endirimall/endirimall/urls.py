"""
Main URL configuration for endirimall project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.contrib.sitemaps.views import sitemap
from core.sitemaps import ProductSitemap, CategorySitemap

# Sitemap configuration
sitemaps = {
    'products': ProductSitemap,
    'categories': CategorySitemap,
}

# URL patterns that support internationalization
urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('deals/', include('deals.urls')),
    path('marketing/', include('marketing.urls')),
    path('', include('core.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    prefix_default_language=False,
)

# Non-internationalized URLs
urlpatterns += [
    path('robots.txt', include('core.urls_robots')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)