from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpRequest
from .forms import SubscriptionForm
from .models import Subscription


def subscribe(request: HttpRequest):
    if request.method == "POST":
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            obj, created = Subscription.objects.get_or_create(email=email)
            if created:
                messages.success(request, "Subscribed successfully!")
            else:
                messages.info(request, "You are already subscribed.")
        else:
            messages.error(request, "Please provide a valid email address.")
    return redirect(request.META.get("HTTP_REFERER", "/"))