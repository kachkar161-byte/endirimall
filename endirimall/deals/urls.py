"""
Deals app URL patterns.
"""
from django.urls import path
from . import views

app_name = 'deals'

urlpatterns = [
    # Product views
    path('', views.product_list, name='product_list'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('store/<slug:slug>/', views.store_detail, name='store_detail'),
    
    # Search and filtering
    path('search/', views.search_products, name='search'),
    path('hot-deals/', views.hot_deals, name='hot_deals'),
    path('featured/', views.featured_products, name='featured_products'),
    
    # User favorites
    path('favorites/', views.favorite_list, name='favorite_list'),
    path('toggle-favorite/', views.toggle_favorite, name='toggle_favorite'),
]