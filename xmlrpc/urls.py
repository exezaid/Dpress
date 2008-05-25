#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Brainaetic: http://www.thenetplanet.com
#Copyright  2008 The Net Planet Srl. All Rights Reserved. 

"""
URL configuration for the xmlrpc app.
"""
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('xmlrpc.views',
                       (r'^$', 'xmlrpc'),
                       (r'^(?P<method_name>[\w\.]+)/$', 'method_help'),
                        url(r'^(?P<method_name>[\w\.]+)/test/$', 
                         view = 'method_test',
                         name = 'xmlrpc_method_test'),
                       )
