from django.shortcuts import render, redirect
from django.views.generic import CreateView, TemplateView, View
from django.http import JsonResponse
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm

from .models import EmailSubscription


class SubscriptionForm(ModelForm):
    """Form for email subscription"""
    class Meta:
        model = EmailSubscription
        fields = ('email',)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': _('Enter your email address')
        })


class SubscribeView(CreateView):
    """View for email subscription"""
    model = EmailSubscription
    form_class = SubscriptionForm
    template_name = 'marketing/subscribe.html'
    success_url = reverse_lazy('core:home')
    
    def form_valid(self, form):
        try:
            # Check if email already exists
            email = form.cleaned_data['email']
            existing_subscription = EmailSubscription.objects.filter(email=email).first()
            
            if existing_subscription:
                if existing_subscription.is_active:
                    messages.info(self.request, _('You are already subscribed to our newsletter.'))
                else:
                    # Reactivate subscription
                    existing_subscription.resubscribe()
                    messages.success(self.request, _('Your subscription has been reactivated!'))
            else:
                # Create new subscription
                form.save()
                messages.success(self.request, _('Thank you for subscribing to our newsletter!'))
            
            return redirect(self.success_url)
            
        except Exception as e:
            messages.error(self.request, _('An error occurred. Please try again.'))
            return self.form_invalid(form)


class SubscribeAPIView(View):
    """API view for AJAX email subscription"""
    
    def post(self, request):
        try:
            email = request.POST.get('email', '').strip()
            
            if not email:
                return JsonResponse({
                    'success': False,
                    'message': str(_('Please enter your email address.'))
                }, status=400)
            
            # Validate email format
            from django.core.validators import validate_email
            from django.core.exceptions import ValidationError
            
            try:
                validate_email(email)
            except ValidationError:
                return JsonResponse({
                    'success': False,
                    'message': str(_('Please enter a valid email address.'))
                }, status=400)
            
            # Check if email already exists
            existing_subscription = EmailSubscription.objects.filter(email=email).first()
            
            if existing_subscription:
                if existing_subscription.is_active:
                    return JsonResponse({
                        'success': False,
                        'message': str(_('You are already subscribed to our newsletter.'))
                    }, status=400)
                else:
                    # Reactivate subscription
                    existing_subscription.resubscribe()
                    message = str(_('Your subscription has been reactivated!'))
            else:
                # Create new subscription
                EmailSubscription.objects.create(email=email)
                message = str(_('Thank you for subscribing to our newsletter!'))
            
            return JsonResponse({
                'success': True,
                'message': message
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(_('An error occurred. Please try again.'))
            }, status=500)


class UnsubscribeView(TemplateView):
    """View for unsubscribing from newsletter"""
    template_name = 'marketing/unsubscribe.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        email = kwargs.get('email')
        
        try:
            subscription = EmailSubscription.objects.get(email=email, is_active=True)
            subscription.unsubscribe()
            context['success'] = True
            context['message'] = _('You have been successfully unsubscribed from our newsletter.')
        except EmailSubscription.DoesNotExist:
            context['success'] = False
            context['message'] = _('Subscription not found or already inactive.')
        
        return context
