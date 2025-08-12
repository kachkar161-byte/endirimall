"""
Core app URL patterns.
"""
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-of-service/', views.terms_of_service, name='terms_of_service'),
    path('newsletter/subscribe/', views.newsletter_subscription, name='newsletter_subscribe'),
    path('sitemap.xml', views.sitemap_xml, name='sitemap_xml'),
]