# -*- encoding: utf-8 -*-

from django import template
from django.contrib.contenttypes.models import ContentTypeManager
from django.conf import  settings

from db import ctm_get

template.add_to_builtins("utils.templatetags.links")
template.add_to_builtins("utils.templatetags.messages")
template.add_to_builtins("blog.templatetags.datelinks")
template.add_to_builtins("typogrify.templatetags.typogrify")

#if getattr(settings, 'ORM_DEBUG'):
    #template.add_to_builtins("debug.templatetags.orm_debug")

ContentTypeManager.get = ctm_get

from django.forms.util import ErrorDict
if 'as_json' not in ErrorDict.__dict__:
    from utils.ajax import as_json
    ErrorDict.as_json = as_json
