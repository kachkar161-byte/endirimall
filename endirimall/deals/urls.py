from django.urls import path
from . import views

app_name = 'deals'

urlpatterns = [
    # Product URLs
    path('', views.ProductListView.as_view(), name='product_list'),
    path('product/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('featured/', views.FeaturedProductsView.as_view(), name='featured_products'),
    
    # Category URLs
    path('category/<slug:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    
    # Store URLs
    path('store/<slug:slug>/', views.StoreDetailView.as_view(), name='store_detail'),
    path('stores/', views.StoreListView.as_view(), name='store_list'),
    
    # Search
    path('search/', views.SearchView.as_view(), name='search'),
    path('api/search/', views.SearchAPIView.as_view(), name='search_api'),
    
    # Favorites
    path('favorites/', views.FavoritesView.as_view(), name='favorites'),
    path('api/toggle-favorite/<int:product_id>/', views.ToggleFavoriteView.as_view(), name='toggle_favorite'),
]