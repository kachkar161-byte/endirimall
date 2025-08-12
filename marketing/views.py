from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils.translation import gettext as _

from .models import Subscription


def subscribe_email(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        if email:
            subscription, created = Subscription.objects.get_or_create(email=email)
            if created:
                messages.success(request, _('Subscribed successfully.'))
            else:
                messages.info(request, _('This email is already subscribed.'))
        else:
            messages.error(request, _('Please provide a valid email.'))
        if request.is_ajax():
            return JsonResponse({'status': 'ok'})
    return redirect(request.META.get('HTTP_REFERER', '/'))
