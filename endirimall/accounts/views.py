from django.shortcuts import render, redirect
from django.views.generic import CreateView, TemplateView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm
from django import forms

from .models import UserProfile


class CustomUserCreationForm(UserCreationForm):
    """Extended user creation form"""
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add CSS classes to form fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name == 'email':
                field.required = True


class UserProfileForm(ModelForm):
    """Form for editing user profile"""
    class Meta:
        model = UserProfile
        fields = ('avatar', 'phone_number', 'date_of_birth', 'preferred_language', 'receive_newsletter')
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add CSS classes to form fields
        for field_name, field in self.fields.items():
            if field_name != 'receive_newsletter':
                field.widget.attrs['class'] = 'form-control'


class CustomLoginView(LoginView):
    """Custom login view with Bootstrap styling"""
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('core:home')
    
    def form_valid(self, form):
        messages.success(self.request, _('Welcome back! You have been logged in successfully.'))
        return super().form_valid(form)


class SignUpView(CreateView):
    """User registration view"""
    form_class = CustomUserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('accounts:login')
    
    def form_valid(self, form):
        messages.success(self.request, _('Account created successfully! Please log in.'))
        return super().form_valid(form)
    
    def dispatch(self, request, *args, **kwargs):
        # Redirect authenticated users
        if request.user.is_authenticated:
            return redirect('core:home')
        return super().dispatch(request, *args, **kwargs)


class ProfileView(LoginRequiredMixin, TemplateView):
    """User profile view"""
    template_name = 'accounts/profile.html'
    login_url = reverse_lazy('accounts:login')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get user's favorites count
        context['favorites_count'] = self.request.user.favorites.count()
        
        # Get recent favorites
        context['recent_favorites'] = self.request.user.favorites.select_related(
            'product__store', 'product__category'
        ).order_by('-created_at')[:5]
        
        return context


class ProfileEditView(LoginRequiredMixin, UpdateView):
    """Edit user profile view"""
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('accounts:profile')
    login_url = reverse_lazy('accounts:login')
    
    def get_object(self):
        # Get or create user profile
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile
    
    def form_valid(self, form):
        messages.success(self.request, _('Profile updated successfully!'))
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add user form for editing basic user info
        if self.request.method == 'POST':
            context['user_form'] = UserForm(self.request.POST, instance=self.request.user)
        else:
            context['user_form'] = UserForm(instance=self.request.user)
        
        return context
    
    def form_valid(self, form):
        # Also save user form
        context = self.get_context_data()
        user_form = context['user_form']
        
        if user_form.is_valid():
            user_form.save()
            form.save()
            messages.success(self.request, _('Profile updated successfully!'))
            return redirect(self.success_url)
        else:
            return self.form_invalid(form)


class UserForm(ModelForm):
    """Form for editing basic user information"""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add CSS classes to form fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name == 'email':
                field.required = True
