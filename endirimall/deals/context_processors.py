from django.contrib.auth.models import AnonymousUser
from .models import Category, Favorite


def categories(request):
    return {"nav_categories": Category.objects.all()}


def favorite_count(request):
    user = request.user
    if isinstance(user, AnonymousUser) or not user.is_authenticated:
        return {"favorite_count": 0}
    return {"favorite_count": Favorite.objects.filter(user=user).count()}