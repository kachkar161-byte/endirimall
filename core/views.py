from django.shortcuts import redirect, render
from django.utils import translation
from django.contrib import messages
from django.conf import settings


def homepage(request):
    """Render the homepage."""
    return render(request, 'core/home.html')


def switch_language(request, language_code):
    """Switch site language and redirect back."""
    if language_code in dict(translation.get_supported_language_variant(lang) for lang in dict(settings.LANGUAGES).keys()):
        translation.activate(language_code)
        request.session[translation.LANGUAGE_SESSION_KEY] = language_code
        messages.success(request, translation.gettext('Language changed successfully.'))
    return redirect(request.META.get('HTTP_REFERER', 'core:home'))
