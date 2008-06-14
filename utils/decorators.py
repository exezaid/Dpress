from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from utils.http import JsonResponse
import os
def theme_template(templatename, theme=None):
    """
    Return a tuple of valid template path
    """
    if not theme:
        theme = settings.THEME
    name = 'themes/%s/%s' %(theme, templatename)
    for dir in settings.TEMPLATE_DIRS:
        test_path = os.path.join(dir, name)
        if os.path.exists(test_path):
            return test_path
     
    return templatename
    
def render_to(template):
    """
    Decorator for Django views that sends returned dict to render_to_response function
    with given template and RequestContext as context instance.

    If view doesn't return dict then decorator simply returns output.
    Additionally view can return two-tuple, which must contain dict as first
    element and string with template name as second. This string will
    override template name, given as parameter

    Parameters:

     - template: template name to use
    """
    def renderer(func):
        def wrapper(request, *args, **kw):
            output = func(request, *args, **kw)
            if isinstance(output, (list, tuple)):
                return render_to_response(theme_template(output[1]), output[0], RequestContext(request))
            elif isinstance(output, dict):
                return render_to_response(theme_template(template), output, RequestContext(request))
            return output
        return wrapper
    return renderer


def ajax_request(func):
    """
    Checks request.method is POST. Return error in JSON in other case.

    If view returned dict, returns JsonResponse with this dict as content.
    """
    def wrapper(request, *args, **kwargs):
        if request.method == 'POST':
            response = func(request, *args, **kwargs)
        else:
            response = {'error': {'type': 403, 'message': 'Accepts only POST request'}}
        if isinstance(response, dict):
            return JsonResponse(response)
        else:
            return response
    return wrapper
