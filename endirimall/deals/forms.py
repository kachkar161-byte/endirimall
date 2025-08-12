"""
Deals app forms for search and filtering.
"""
from django import forms
from django.utils.translation import gettext_lazy as _


class ProductSearchForm(forms.Form):
    """
    Form for searching products.
    """
    q = forms.CharField(
        label=_('Axtarış'),
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Məhsul, mağaza və ya kateqoriya axtarın...'),
            'aria-label': _('Axtarış'),
        })
    )
    
    category = forms.ChoiceField(
        label=_('Kateqoriya'),
        required=False,
        choices=[('', _('Bütün kateqoriyalar'))],
        widget=forms.Select(attrs={
            'class': 'form-select',
        })
    )
    
    store = forms.ChoiceField(
        label=_('Mağaza'),
        required=False,
        choices=[('', _('Bütün mağazalar'))],
        widget=forms.Select(attrs={
            'class': 'form-select',
        })
    )
    
    sort_by = forms.ChoiceField(
        label=_('Sıralama'),
        required=False,
        choices=[
            ('newest', _('Ən yeni')),
            ('price_low', _('Qiymət (aşağıdan yuxarıya)')),
            ('price_high', _('Qiymət (yuxarıdan aşağıya)')),
            ('discount', _('Ən böyük endirim')),
        ],
        widget=forms.Select(attrs={
            'class': 'form-select',
        })
    )
    
    min_price = forms.DecimalField(
        label=_('Minimum qiymət'),
        required=False,
        min_value=0,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': _('Min qiymət'),
        })
    )
    
    max_price = forms.DecimalField(
        label=_('Maksimum qiymət'),
        required=False,
        min_value=0,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': _('Max qiymət'),
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Dynamically populate category and store choices
        from .models import Category, Store
        
        categories = Category.objects.filter(is_active=True)
        stores = Store.objects.filter(is_active=True)
        
        self.fields['category'].choices = [('', _('Bütün kateqoriyalar'))] + [
            (cat.slug, cat.name) for cat in categories
        ]
        
        self.fields['store'].choices = [('', _('Bütün mağazalar'))] + [
            (store.slug, store.name) for store in stores
        ]
    
    def clean(self):
        cleaned_data = super().clean()
        min_price = cleaned_data.get('min_price')
        max_price = cleaned_data.get('max_price')
        
        if min_price and max_price and min_price > max_price:
            raise forms.ValidationError(_('Minimum qiymət maksimum qiymətdən böyük ola bilməz'))
        
        return cleaned_data