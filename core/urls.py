from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('home/', views.homepage, name='home'),
    path('switch-language/<str:language_code>/', views.switch_language, name='switch_language'),
]