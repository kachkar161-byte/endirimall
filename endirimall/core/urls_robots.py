"""
Robots.txt URL pattern.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.robots_txt, name='robots_txt'),
]