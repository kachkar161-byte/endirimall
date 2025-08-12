from django.urls import path
from .views import subscribe

app_name = "marketing"

urlpatterns = [
    path("subscribe/", subscribe, name="subscribe"),
]