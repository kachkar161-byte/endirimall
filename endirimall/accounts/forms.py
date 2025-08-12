"""
Accounts app forms for user registration and profile management.
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class CustomUserCreationForm(UserCreationForm):
    """
    Custom user creation form with additional fields.
    """
    email = forms.EmailField(
        label=_('Email'),
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': _('Email ünvanınızı daxil edin'),
        })
    )
    
    first_name = forms.CharField(
        label=_('Ad'),
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Adınızı daxil edin'),
        })
    )
    
    last_name = forms.CharField(
        label=_('Soyad'),
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Soyadınızı daxil edin'),
        })
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Customize password fields
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': _('İstifadəçi adınızı daxil edin'),
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': _('Şifrənizi daxil edin'),
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': _('Şifrənizi təsdiqləyin'),
        })
        
        # Customize labels
        self.fields['username'].label = _('İstifadəçi adı')
        self.fields['password1'].label = _('Şifrə')
        self.fields['password2'].label = _('Şifrə təsdiqi')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_('Bu email ünvanı artıq istifadə olunub'))
        return email


class CustomUserChangeForm(UserChangeForm):
    """
    Custom user change form for profile updates.
    """
    email = forms.EmailField(
        label=_('Email'),
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
        })
    )
    
    first_name = forms.CharField(
        label=_('Ad'),
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )
    
    last_name = forms.CharField(
        label=_('Soyad'),
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['username'].label = _('İstifadəçi adı')


class ProfileUpdateForm(forms.ModelForm):
    """
    Form for updating user profile information.
    """
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'first_name': _('Ad'),
            'last_name': _('Soyad'),
            'email': _('Email'),
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError(_('Bu email ünvanı artıq istifadə olunub'))
        return email


class PasswordChangeForm(forms.Form):
    """
    Form for changing user password.
    """
    current_password = forms.CharField(
        label=_('Cari şifrə'),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Cari şifrənizi daxil edin'),
        })
    )
    
    new_password1 = forms.CharField(
        label=_('Yeni şifrə'),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Yeni şifrənizi daxil edin'),
        })
    )
    
    new_password2 = forms.CharField(
        label=_('Yeni şifrə təsdiqi'),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Yeni şifrənizi təsdiqləyin'),
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')
        
        if new_password1 and new_password2:
            if new_password1 != new_password2:
                raise forms.ValidationError(_('Yeni şifrələr uyğun gəlmir'))
        
        return cleaned_data