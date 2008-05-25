from django.template import Library, Context, loader

register = Library()
@register.inclusion_tag('tagging/tag_cloud.html')
def render_tag_cloud(tags):
    return {'tags': tags}


@register.inclusion_tag('tagging/tag_string.html')
def render_tag_string(tags):
    return {'tags': tags}
