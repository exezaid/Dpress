from docutils import nodes
from docutils.parsers.rst import directives
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
import docutils
import re
class highlight_block(nodes.General, nodes.Text):pass

from docutils.writers.html4css1 import Writer, HTMLTranslator

from django.template.loader import render_to_string

pygments_formatter = HtmlFormatter()

def r_space(m):
    return len(m.group()) * '&nbsp;'

re_space = re.compile(r'^[ ]+', re.MULTILINE)
def code(name, arguments, options, content, lineno,
          content_offset, block_text, state, state_machine):
    global g_data
    
    if len(arguments) > 0:
        lang = arguments[0]
    else:
        lang = ''
    style, text = highlight('\n'.join(content), lang)
    text = re_space.sub(r_space, text)
    g_data.g_style[lang] = style
    return [highlight_block(text)]

code.content = 1
code.arguments = (0, 1, 1)
directives.register_directive('code', code)

def photologue_rst( name, arguments, options, content, lineno,
             content_offset, block_text, state, state_machine ):
  """
  The code-block directive provides syntax highlighting for blocks
  of code.  It is used with the the following syntax::
  
  .. photologue:: 1
    
  The directive requires the name of a language supported by SilverCity
  as its only argument.  All code in the indented block following
  the directive will be colourized.  Note that this directive is only
  supported for HTML writers.
  """
  from photologue.models import Photo
  image_id = arguments[0]
  try:
      photo = Photo.objects.get(pk=int(image_id))
  except Photo.DoesNotExist:
      return []
  return [docutils.nodes.raw('',render_to_string('templatetags/rest_photologue.html',{'photo':photo}), format = 'html')]

photologue_rst.arguments = (1,0,0)
photologue_rst.options = {'photologue' : docutils.parsers.rst.directives.unchanged }
photologue_rst.content = 1
  
directives.register_directive( 'photologue', photologue_rst )