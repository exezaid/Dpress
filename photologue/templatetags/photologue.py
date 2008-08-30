from django import template
from django.core import template_loader
import re
from django.contrib.contenttypes.models import ContentType

register = template.Library()

@register.simple_tag
def next_in_gallery(photo, gallery):
    next = photo.get_next_in_gallery(gallery)
    if next:
        return '<a title="%s" href="%s"><img src="%s"/></a>' % (next.title, next.get_absolute_url(), next.get_thumbnail_url())
    return ""
    
@register.simple_tag
def previous_in_gallery(photo, gallery):
    prev = photo.get_previous_in_gallery(gallery)
    if prev:
        return '<a title="%s" href="%s"><img src="%s"/></a>' % (prev.title, prev.get_absolute_url(), prev.get_thumbnail_url())
    return ""

class LatestGalleries(template.Node):
  def __init__(self, format_string, var_name):
    self.format_string = format_string
    self.var_name = var_name
  
  def render(self, context):
    content_type = ContentType.objects.get(app_label='photologue', model='gallery')
    Gallery = content_type.model_class()
    galleries = Gallery.objects.filter(is_public=True).order_by('-date_added')[:int(self.format_string)]
    context[self.var_name] = galleries
    return ''

@register.tag(name='get_latest_galleries')
def do_get_latest_galleries(parser, token):
  """
  Gets any number of latest galleries and stores them in a variable.
  
  Syntax::
  
    {% get_latest_galleries [limit] as [var_name] %}
  
  Example usage::
    
    {% get_latest_galleries 10 as latest_gallery_list %}
  """
  try:
    tag_name, arg = token.contents.split(None, 1)
  except ValueError:
    raise template.TemplateSyntaxError, "%s tag requires arguments" % token.contents.split()[0]
  m = re.search(r'(\d+) as (\w+)', arg)
  if not m:
    raise template.TemplateSyntaxError, "%s tag had invalid arguments" % tag_name
  format_string, var_name = m.groups()
  return LatestGalleries(format_string, var_name)

class LatestPhotos(template.Node):
  def __init__(self, format_string, var_name):
    self.format_string = format_string
    self.var_name = var_name
  
  def render(self, context):
    content_type = ContentType.objects.get(app_label='photologue', model='photo')
    Photo = content_type.model_class()
    photos = Photo.objects.filter(is_public=True).order_by('-date_added')[:int(self.format_string)]
    context[self.var_name] = photos
    return ''

@register.tag(name='get_latest_photos')
def do_get_latest_photos(parser, token):
  """
  Gets any number of latest photos and stores them in a variable.
  
  Syntax::
  
    {% get_latest_photos [limit] as [var_name] %}
  
  Example usage::
    
    {% get_latest_photos 10 as latest_gallery_list %}
  """
  try:
    tag_name, arg = token.contents.split(None, 1)
  except ValueError:
    raise template.TemplateSyntaxError, "%s tag requires arguments" % token.contents.split()[0]
  m = re.search(r'(\d+) as (\w+)', arg)
  if not m:
    raise template.TemplateSyntaxError, "%s tag had invalid arguments" % tag_name
  format_string, var_name = m.groups()
  return LatestPhotos(format_string, var_name)
