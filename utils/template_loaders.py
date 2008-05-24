from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.template import TemplateDoesNotExist
from django.utils._os import safe_join

def get_theme_template(template_name, template_dirs=None):
    """
    Template loader, which returns template path accordingly to THEME setting.

    Requires PROJECT_ROOT setting.
    """
    if not (hasattr(settings, 'PROJECT_ROOT') and hasattr(settings, 'THEME')):
        raise ImproperlyConfigured("There is no PROJECT_ROOT or THEME setting")
    filepath = safe_join(settings.PROJECT_ROOT, 'themes', settings.THEME, template_name)
    try:
        return (open(filepath).read().decode(settings.FILE_CHARSET), filepath)
    except IOError:
        raise TemplateDoesNotExist("Tried %s" % filepath)

get_theme_template.is_usable = True
