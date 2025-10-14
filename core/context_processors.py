from django.conf import settings

from core.mt_modules import get_available_modules

def global_settings(request):
    return {
        'DEBUG': settings.DEBUG,
        "BAKE_MODE": settings.BAKE_MODE,
        "AVAILABLE_MODULES": get_available_modules(),
    }