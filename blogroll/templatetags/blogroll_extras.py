from django import template

from blogroll.models import Link

register = template.Library()

@register.inclusion_tag('blogroll/links.html')
def blogroll_links():
    """
    Include blogroll: list of links controlled from admin interface, including
    XFN information.

    Renders 'blogroll/links.html' template at the point of inclusion.
    """
    
    links = Link.objects.all()
    return {'links': links,
            }
