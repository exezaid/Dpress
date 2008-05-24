from django.core.urlresolvers import reverse as _reverse
from django.shortcuts import _get_queryset, get_object_or_404
from django.http import Http404
from markdown import Markdown

from utils.exceptions import Ajax404
from typogrify.templatetags.typogrify import typogrify


def reverse(view_name, *args, **kwargs):
    return _reverse(view_name, args=args, kwargs=kwargs)


def get_object_or_404_ajax(*args, **kwargs):
    try:
        return get_object_or_404(*args, **kwargs)
    except Http404, e:
        raise Ajax404, e


def get_object_or_none(klass, *args, **kwargs):
    """
    Uses get() to return an object or None if the object does not exist.

    klass may be a Model, Manager, or QuerySet object. All other passed
    arguments and keyword arguments are used in the get() query.

    Note: Like with get(), an MultipleObjectsReturned will be raised if more than one
    object is found.
    """
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return None
