from django.urls import path
from . import views

app_name = 'deals'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('favorite/toggle/', views.toggle_favorite, name='toggle_favorite'),
    path('search/', views.search_products, name='search_products'),
]