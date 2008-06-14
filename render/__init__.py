"""Realisation of rendering different markup languages"""

from utils.markdown import Markdown
from utils.bbcode import bb2xhtml

from render import textparser
from render.morefixer import more_fix
from typogrify.templatetags.typogrify import typogrify
import rest

class RenderException(Exception):
    """Can't render"""
    pass


def render(content, render_method, unsafe=False):
    renderer = Renderer(content, render_method, unsafe)
    return renderer.render()


class Renderer(object):
    def __init__(self, content, render_method, unsafe=False):
        self.content = content.strip()
        self.render_method = render_method
        self.unsafe = unsafe

    def render(self):
        try:
            renderer = getattr(self, 'get_%s_render' % self.render_method)()
            return unicode(typogrify(more_fix(renderer(self.content))))
        except AttributeError:
            import traceback
            traceback.print_exc()
            raise RenderException(u"Unknown render method: '%s'" % self.render_method)

    def get_markdown_render(self):
        md = Markdown(extensions=['footnotes', 'abbr'], safe_mode=not self.unsafe)
        return md.convert

    def get_bbcode_render(self):
        return bb2xhtml

    def get_text_render(self):
        return textparser.to_html

    def get_html_render(self):
        return lambda x: x

    def get_html_br_render(self):
        return textparser.add_br

    def get_html_render(self):
        return lambda x: x

    def get_rest_render(self):
        from django.contrib.markup.templatetags.markup import restructuredtext
        return restructuredtext
