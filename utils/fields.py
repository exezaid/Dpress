# -*- coding:utf-8 -*-

from django.db.models import OneToOneField
from django.db.models.fields.related import SingleRelatedObjectDescriptor
from django.db import models
import datetime

class AddedDateTimeField(models.DateTimeField):
    def __init__(self, **kwargs):
        kwargs['editable'] = False
        kwargs['blank'] = True
        kwargs['null'] = True
        models.DateTimeField.__init__(self, **kwargs)

    def get_internal_type(self):
        return models.DateTimeField.__name__
    def pre_save(self, model_instance, add):
        if model_instance.id is None or (getattr(model_instance, self.attname) is None):
            return datetime.datetime.now()
        else:
            return getattr(model_instance, self.attname)

class ModifiedDateTimeField(models.DateTimeField):
    def get_internal_type(self):
        return models.DateTimeField.__name__
    def pre_save(self, model_instance, add):
        return datetime.datetime.now()

class AutoSingleRelatedObjectDescriptor(SingleRelatedObjectDescriptor):
    def __get__(self, instance, instance_type=None):
        try:
            return super(AutoSingleRelatedObjectDescriptor, self).__get__(instance, instance_type)
        except self.related.model.DoesNotExist:
            obj = self.related.model(**{self.related.field.name: instance})
            obj.save()
            return obj

class AutoOneToOneField(OneToOneField):
    '''
    OneToOneField, which creates related object for first call
    from parent, if it does not exist.
    '''
    def contribute_to_related_class(self, cls, related):
        setattr(cls, related.get_accessor_name(), AutoSingleRelatedObjectDescriptor(related))
        if not cls._meta.one_to_one_field:
            cls._meta.one_to_one_field = self
