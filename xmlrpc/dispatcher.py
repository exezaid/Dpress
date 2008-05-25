#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Copyright  2008 Alberto Paro <alberto@ingparo.it>
"""
XML-RPC dispatcher with full introspection and multicall support.
"""

import sys
import xmlrpclib
from utils import signature
from xml.parsers import expat


class Dispatcher:
    """
    XML-RPC dispatcher with full introspection and multicall support.
    """

    def __init__(self, allow_none=False, encoding=None):
        self.funcs = {
            'system.listMethods': self.list_methods,
            'system.methodSignature': self.method_signature,
            'system.methodHelp': self.method_help,
            'system.multicall': self.multicall,
            }
        self.allow_none = allow_none
        self.encoding = encoding

    def register_function(self, function, name = None):
        """
        Registers a function to respond to XML-RPC requests.

        The optional name argument can be used to set a Unicode name
        for the function.
        """
        if name is None:
            name = function.__name__
        self.funcs[name] = function

    @signature(list)
    def list_methods(self, http_request):
        """
        Returns a list of the methods supported by the server.
        """
        methods = self.funcs.keys()
        methods.sort()
        return methods

    @signature(list, str)
    def method_signature(self, http_request, method_name):
        """
        Returns a list describing the possible signatures of the
        method.
        """
        if method_name not in self.funcs:
            return 'method not found'
        method = self.funcs[method_name]
        if hasattr(method, '_signature'):
            result = []
            for x in method._signature:
                if x is None:
                    result.append('void')
                elif x is str:
                    result.append('string')
                else:
                    result.append(x.__name__)
            return [result]

    @signature(list, str)
    def method_signature_names(self, http_request, method_name):
        """
        Returns a list describing the possible name signatures of the
        method.
        """
        from brainaetic.utils.Signature import Signature
        if method_name not in self.funcs:
            return 'method not found'
        method = self.funcs[method_name]
        f = Signature(method)
#        print "ordinary arglist:", f.ordinary_args()
#        print "special_args:", f.special_args()
#        print "full_arglist:", f.full_arglist()
#        print "defaults:", f.defaults()
#        print "signature:", f
        return f.full_arglist()

    @signature(str, str)
    def method_help(self, http_request, method_name):
        """
        Returns a string containing documentation for the specified
        method.
        """
        if method_name not in self.funcs:
            return 'method not found'
        method = self.funcs[method_name]
        lines = method.__doc__.splitlines()
        indent = min([len(line) - len(line.lstrip())
                      for line in lines if line.strip()])
        lines = [line[indent:] for line in lines]
        return '\n'.join(lines).strip()

    @signature(list, list)
    def multicall(self, http_request, call_list):
        """
        Allows the caller to package multiple XML-RPC calls into a
        single request.
        """
        results = []
        for call in call_list:
            method = call['methodName']
            params = call['params']
            result = self.dispatch(method, http_request, params)
            results.append([result])
        return results

    def dispatch(self, method, http_request, params):
        """
        Call a registered XML-RPC method.
        """
        if not method in self.funcs:
            method = method.replace('.', '_')
            if not method in self.funcs:
                 raise xmlrpclib.Fault(404,
                    u'method "%s" is not supported' % method)
        func = self.funcs[method]
        response = func(http_request, *params)
#        if instance(response, xmlrpclib.Fault):
#            return response
        return (response, )

    def dispatch_and_marshal(self, method, http_request, params):
        """
        Call a registered XML-RPC method and marshal the response.
        """
        try:
            response = self.dispatch(method, http_request, params)
            response = xmlrpclib.dumps(response, methodresponse=True,
                allow_none=self.allow_none, encoding=self.encoding)
        except xmlrpclib.Fault, fault:
            response = xmlrpclib.dumps(fault,
                allow_none=self.allow_none, encoding=self.encoding)
        except:
            response = xmlrpclib.dumps(
                xmlrpclib.Fault(500,
                    u'%s:%s' % (sys.exc_type, sys.exc_value)),
                allow_none=self.allow_none, encoding=self.encoding)
        return response

    def dispatch_request(self, http_request):
        """Unmarshal and run an XML-RPC request."""
        try:
            params, method = xmlrpclib.loads(http_request.raw_post_data)
        except expat.ExpatError, error:
            return xmlrpclib.dumps(
                xmlrpclib.Fault(400, u"XML parser error: %s" % str(error)))
        return self.dispatch_and_marshal(method, http_request, params)
