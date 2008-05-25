import os.path

from django.conf import settings
from django.contrib.sites.models import Site
from blog.models import Post

def settings_vars(request):
    return {
        'MEDIA_URL': settings.MEDIA_URL,
        'THEME_MEDIA_URL': settings.THEME_MEDIA_URL,
        'settings': settings,
        }

def featured_posts(request):
    return {
        'featured_posts': Post.featured_objects.all()
    }
