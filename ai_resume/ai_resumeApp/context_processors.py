from django.conf import settings

def render_environment(request):
    return {
        'IS_RENDER': getattr(settings, 'IS_RENDER', False)
    }