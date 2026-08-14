"""Language activation middleware.

Reads the visitor's language choice from the session or the ``django_language``
cookie (set by Django's ``set_language`` view) and exposes it on ``request`` as
``request.LANGUAGE_CODE``. This drives the ``{% trans %}`` template tag (see
``user/templatetags/i18n_extras.py``) and the ``LANGUAGE_CODE`` template
variable.
"""

from django.conf import settings


class SimpleLocaleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        supported = {code for code, _ in getattr(settings, "LANGUAGES", [])}

        language = (
            request.session.get("django_language")
            if hasattr(request, "session")
            else None
        )
        if not language:
            language = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME)

        if not language or language not in supported:
            language = settings.LANGUAGE_CODE

        request.LANGUAGE_CODE = language

        response = self.get_response(request)
        return response