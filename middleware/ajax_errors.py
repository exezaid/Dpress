"""
AJAX Middleware

Catches common errors in AJAX views.
"""

from utils.http import JsonResponse
from utils.exceptions import *

class AjaxMiddleware:

    def process_exception(self, request, exception):
        if not isinstance(exception, AjaxException):
            return None
        if isinstance(exception, AjaxDataException):
            return JsonResponse(exception.data)
        if isinstance(exception, Ajax404):
            return JsonResponse({'error': {'type': 404, 'message': exception.message}})
