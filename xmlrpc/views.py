#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Copyright  2008 Alberto Paro <alberto@ingparo.it>
"""
Self-documenting XML-RPC interface.
"""
from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.utils.safestring import mark_safe
from django.conf import settings
from dispatcher import Dispatcher
from forms import TypedForm

RST_SETTINGS = {
    'initial_header_level': 2,
    'doctitle_xform': False,
    'docinfo_xform': False,
    }


def xmlrpc(http_request):
    """
    XML-RPC interface (for POST requests) and automatic human-readable
    HTML documentation (for GET requests).
    """
    try:
        is_post_request = len(http_request.POST)
    except (IOError, SystemError), error:
        return HttpResponse(content=str(error), status=500)
    if is_post_request:
        response = HttpResponse()
        response.write(dispatcher.dispatch_request(http_request))
        response['Content-length'] = str(len(response.content))
        return response
    else:
        method_list = dispatcher.list_methods(http_request)
        return render_to_response('xmlrpc/method_list.html', locals(),
            context_instance=RequestContext(http_request))


def method_help(http_request, method_name):
    """
    Display automatic help about an XML-RPC method.
    """
    if len(http_request.POST):
        raise Http404 # Don't POST here, only GET documentation
    if method_name not in dispatcher.list_methods(http_request):
        raise Http404 # Method not found
    signatures = dispatcher.method_signature(http_request, method_name)
    signature_lines = []
    for signature in signatures:
        result = signature[0]
        params = signature[1:]
        signature_lines.append('%s(%s) => %s' % (
            method_name, ', '.join(params), result))
    docstring = dispatcher.method_help(http_request, method_name)
    try:
        from docutils import core
        parts = core.publish_parts(
            source=docstring, writer_name='html',
            settings_overrides=RST_SETTINGS)
        docstring = parts['html_body']
    except ImportError:
        docstring = u'<pre>\n%s\n</pre>\n' % docstring
    for method in dispatcher.funcs:
        docstring = docstring.replace(
            method, u'<a href="../%s/">%s</a>' % (method, method))
    docstring = mark_safe(docstring)
    return render_to_response('xmlrpc/method_help.html', locals(),
        context_instance=RequestContext(http_request))

def method_test(http_request, method_name):
    """
    Display test XML-RPC method.
    """
#    if len(http_request.POST):
#        raise Http404 # Don't POST here, only GET documentation
    if method_name not in dispatcher.list_methods(http_request):
        raise Http404 # Method not found
    print http_request
    signatures = dispatcher.method_signature(http_request, method_name)
    signatures_names = dispatcher.method_signature_names(http_request, method_name)
    signature_lines = []
    for signature in signatures:
        result = signature[0]
        params = signature[1:]
        signature_lines.append('%s(%s) => %s' % (
            method_name, ', '.join(params), result))
    if http_request.POST:
        form = TypedForm(signatures_names[1:], params, http_request.POST)
        if form.is_valid():
            d = form.cleaned_data
            from xmlrpclib import ServerProxy
            server = ServerProxy('http://%s:%s/xmlrpc/' % (http_request.META['REMOTE_ADDR'], http_request.META['SERVER_PORT']))
            mmethod = getattr(server, 'method_name')
            print d
            result = mmethod(**d)
    else:
        form = TypedForm(signatures_names[1:], params)
    return render_to_response('xmlrpc/method_test.html', locals(),
        context_instance=RequestContext(http_request))


dispatcher = Dispatcher()

try:
    try:
        module = __import__('metaweblog', globals(), locals(), [])
    except ImportError, error:
        #if  'no module named xmlrpc' in str(error).lower():
        raise

    for name, item in module.__dict__.items():
        if hasattr(item, '_signature'):
            function_name = '%s' % (name)
            dispatcher.register_function(item, function_name)
except ImportError, error:
        pass
