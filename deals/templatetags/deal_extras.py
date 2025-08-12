from django import template
from deals.models import Favorite

register = template.Library()


@register.filter
def favorite_icon(product, user):
    """Return appropriate bootstrap icon class based on favorite status."""
    if not user.is_authenticated:
        return 'bi-heart'
    is_favorite = Favorite.objects.filter(user=user, product=product).exists()
    return 'bi-heart-fill text-danger' if is_favorite else 'bi-heart'