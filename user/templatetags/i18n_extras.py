from django import template
from django.conf import settings

from config.i18n import AVAILABLE_LANGUAGES, translate

register = template.Library()


def _current_language(context):
    request = context.get("request")
    lang = getattr(request, "LANGUAGE_CODE", None)
    if not lang:
        lang = context.get("LANGUAGE_CODE") or settings.LANGUAGE_CODE
    return lang


@register.simple_tag(takes_context=True)
def trans(context, text):
    """Translate the given literal by the current page language."""
    text = (text or "").strip()
    return translate(_current_language(context), text)


@register.simple_tag(takes_context=True)
def current_language(context):
    """Current ISO language code (e.g. 'en', 'ru', 'uz')."""
    return _current_language(context)


@register.simple_tag
def available_languages():
    """List of supported (code, short_label) tuples for the switcher."""
    return AVAILABLE_LANGUAGES


@register.simple_tag(takes_context=True)
def language_is(context, code):
    """Return True when the active language equals ``code``."""
    return _current_language(context) == code