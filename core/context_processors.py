from django.conf import settings

def global_settings(request):
    return {
        'DEBUG': settings.DEBUG,
        "BAKE_MODE": settings.BAKE_MODE,
    }