from django.urls import path
from . import views

app_name = "deals"

urlpatterns = [
    path("", views.product_list, name="product_list"),
    path("category/<slug:slug>/", views.product_list, name="product_list_by_category"),
    path("store/<slug:slug>/", views.product_list, name="product_list_by_store"),
    path("search/", views.search, name="search"),
    path("fav/<int:product_id>/toggle/", views.toggle_favorite, name="toggle_favorite"),
    path("<slug:store_slug>/<slug:slug>/", views.product_detail, name="product_detail"),
]