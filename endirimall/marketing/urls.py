from django.urls import path
from . import views

app_name = 'marketing'

urlpatterns = [
    path('subscribe/', views.SubscribeView.as_view(), name='subscribe'),
    path('unsubscribe/<str:email>/', views.UnsubscribeView.as_view(), name='unsubscribe'),
    path('api/subscribe/', views.SubscribeAPIView.as_view(), name='subscribe_api'),
]