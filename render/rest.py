from docutils import nodes, parsers
from docutils.parsers.rst import directives
import docutils
import re
class highlight_block(nodes.General, nodes.Text):pass

from docutils.writers.html4css1 import Writer, HTMLTranslator

from django.template.loader import render_to_string


def r_space(m):
    return len(m.group()) * '&nbsp;'

def get_highlighter(language):

    from pygments import lexers, util, highlight, formatters
    import StringIO

    try:
        lexer = lexers.get_lexer_by_name(language)
    except util.ClassNotFound:
        return None

    formatter = formatters.get_formatter_by_name('html')
    def _highlighter(code):
        outfile = StringIO.StringIO()
        highlight(code, lexer, formatter, outfile)
        return outfile.getvalue()
    return _highlighter

re_space = re.compile(r'^[ ]+', re.MULTILINE)
#def code(name, arguments, options, content, lineno,
#          content_offset, block_text, state, state_machine):
#    global g_data
#    
#    if len(arguments) > 0:
#        lang = arguments[0]
#    else:
#        lang = ''
#    style, text = highlight('\n'.join(content), lang)
#    text = re_space.sub(r_space, text)
#    g_data.g_style[lang] = style
#    return [highlight_block(text)]

# Docutils directives:
def code(name, arguments, options, content, lineno,
               content_offset, block_text, state, state_machine):
    """
    The code directive provides syntax highlighting for blocks
    of code.  It is used with the the following syntax::

    .. code:: python

       import sys
       def main():
           sys.stdout.write("Hello world")

    Currently support languages: python (requires pygments),
    haskell (requires HsColour), anything else supported by pygments
    """


    language = arguments[0]
    highlighter = get_highlighter(language)
    if highlighter is None:
        error = state_machine.reporter.error(
            'The "%s" directive does not support language "%s".' % (name, language),
            nodes.literal_block(block_text, block_text), line=lineno)

    if not content:
        error = state_machine.reporter.error(
            'The "%s" block is empty; content required.' % (name),
            nodes.literal_block(block_text, block_text), line=lineno)
        return [error]

    include_text = highlighter("\n".join(content))
    html = '<div class="codeblock %s">\n%s\n</div>\n' % (language, include_text)
    raw = nodes.raw('',html, format='html')
    return [raw]

code.content = 1
code.options = {'language' : parsers.rst.directives.unchanged }
code.arguments = (1,0,0)


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