"""
Accounts app views for user authentication and profile management.
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm as DjangoPasswordChangeForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import CustomUserCreationForm, ProfileUpdateForm, PasswordChangeForm


class SignUpView(CreateView):
    """
    User registration view.
    """
    form_class = CustomUserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('core:home')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        # Log the user in after successful registration
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        if user:
            login(self.request, user)
            messages.success(self.request, _('Uğurla qeydiyyatdan keçdiniz!'))
        return response


def signin(request):
    """
    User login view.
    """
    if request.user.is_authenticated:
        return redirect('core:home')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, _('Uğurla daxil oldunuz!'))
                next_url = request.GET.get('next', 'core:home')
                return redirect(next_url)
            else:
                messages.error(request, _('İstifadəçi adı və ya şifrə yanlışdır'))
        else:
            messages.error(request, _('Daxil etdiyiniz məlumatları yoxlayın'))
    else:
        form = AuthenticationForm()
    
    context = {
        'form': form,
        'page_title': _('Daxil ol'),
    }
    
    return render(request, 'accounts/signin.html', context)


@login_required
def profile(request):
    """
    User profile view.
    """
    context = {
        'page_title': _('Profil'),
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def profile_edit(request):
    """
    Edit user profile view.
    """
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _('Profil uğurla yeniləndi!'))
            return redirect('accounts:profile')
        else:
            messages.error(request, _('Xəta baş verdi. Məlumatları yoxlayın'))
    else:
        form = ProfileUpdateForm(instance=request.user)
    
    context = {
        'form': form,
        'page_title': _('Profili Redaktə Et'),
    }
    
    return render(request, 'accounts/profile_edit.html', context)


@login_required
def change_password(request):
    """
    Change user password view.
    """
    if request.method == 'POST':
        form = DjangoPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, _('Şifrə uğurla dəyişdirildi!'))
            return redirect('accounts:profile')
        else:
            messages.error(request, _('Xəta baş verdi. Məlumatları yoxlayın'))
    else:
        form = DjangoPasswordChangeForm(request.user)
    
    context = {
        'form': form,
        'page_title': _('Şifrəni Dəyişdir'),
    }
    
    return render(request, 'accounts/change_password.html', context)


@login_required
def delete_account(request):
    """
    Delete user account view.
    """
    if request.method == 'POST':
        # Delete the user account
        user = request.user
        user.delete()
        messages.success(request, _('Hesabınız uğurla silindi'))
        return redirect('core:home')
    
    context = {
        'page_title': _('Hesabı Sil'),
    }
    return render(request, 'accounts/delete_account.html', context)