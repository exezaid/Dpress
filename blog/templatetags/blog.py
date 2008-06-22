from django.template import Library, Context, loader
from django import template
from django.core import template_loader
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
import re
Post = models.get_model('blog', 'post')

register = template.Library()

class LatestPosts(template.Node):
  def __init__(self, format_string, var_name):
    self.format_string = format_string
    self.var_name = var_name
  
  def render(self, context):
    posts = Post.objects.all()[:int(self.format_string)]
    context[self.var_name] = posts
    return ''

@register.tag(name='get_latest_posts')
def do_get_latest_posts(parser, token):
  """
  Gets any number of latest posts and stores them in a varable.
  
  Syntax::
  
    {% get_latest_posts [limit] as [var_name] %}
  
  Example usage::
    
    {% get_latest_posts 10 as latest_post_list %}
  """
  try:
    tag_name, arg = token.contents.split(None, 1)
  except ValueError:
    raise template.TemplateSyntaxError, "%s tag requires arguments" % token.contents.split()[0]
  m = re.search(r'(\d+) as (\w+)', arg)
  if not m:
    raise template.TemplateSyntaxError, "%s tag had invalid arguments" % tag_name
  format_string, var_name = m.groups()
  return LatestPosts(format_string, var_name)


@register.inclusion_tag('tagging/tag_cloud.html')
def render_tag_cloud(tags):
    return {'tags': tags}


@register.inclusion_tag('tagging/tag_string.html')
def render_tag_string(tags):
    return {'tags': tags}
