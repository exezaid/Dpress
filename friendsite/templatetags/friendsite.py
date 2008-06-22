from django import template
from django.db import models
import re
FriendSite = models.get_model('friendsite', 'friendsite')

register = template.Library()

class GetFriendSites(template.Node):
  def __init__(self, format_string, var_name):
    self.format_string = format_string
    self.var_name = var_name
  
  def render(self, context):
    if self.format_string:
        friendSites = FriendSite.objects.all()[:int(self.format_string)]
    else:
        friendSites = FriendSite.objects.all()
        
    context[self.var_name] = friendSites
    return ''

@register.tag(name='get_friendsites')
def get_friendsites(parser, token):
  """
  Gets any number of friendsites and stores them in a varable.
  
  Syntax::
  
    {% get_get_friendsites [limit] as [var_name] %}
  
  Example usage::
    
    {% get_friendsites 10 as friendsites_list %}
  """
  try:
    tag_name, arg = token.contents.split(None, 1)
  except ValueError:
    raise template.TemplateSyntaxError, "%s tag requires arguments" % token.contents.split()[0]
  m = re.search(r'(.*?) as (\w+)', arg)
  if not m:
    raise template.TemplateSyntaxError, "%s tag had invalid arguments" % tag_name
  format_string, var_name = m.groups()
  return GetFriendSites(format_string[0], var_name)
