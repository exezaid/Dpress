from django.db import models
from django.conf import settings
from django.utils.html import strip_tags
from blog.models import RENDER_METHODS
from render import render
#from django.contrib.contenttypes import generic

SIDE_CHOICES = (
    (1, 'Left'),
    (2, 'Right'),
)


class TextBlock(models.Model):
    code = models.CharField(verbose_name=u'Unique system code', max_length=128, unique=True)
    name = models.CharField(verbose_name=u'Block name', max_length=255, blank=True)
    text = models.TextField(verbose_name=u'Block content', blank=True)
    render_method = models.CharField(verbose_name=u'Render method', max_length=15, choices=RENDER_METHODS, default=settings.RENDER_METHOD)
    html = models.TextField(verbose_name=u'HTML', blank=True)
    comment = models.TextField(blank=True, max_length=255, verbose_name=u'Comments about block')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return "%s - %s" % (self.code, self.comment)
        
    def save(self):
        self.text = self.text.strip()
        #if not self.render_method:
            #self.render_method = settings.RENDER_METHOD
        self.html = render(self.text, self.render_method, unsafe=True)
        super(TextBlock, self).save()

    class Meta:
        verbose_name = u'text block'
        verbose_name_plural = u'text blocks'
        get_latest_by = "updated_on"
        ordering = ['-created_on']


    class Admin:
        list_display = ('code', 'name', 'comment',)
        search_fields = ('name', 'text')

class SideBlock(models.Model):
    name = models.CharField(verbose_name=u'Unique Block name', max_length=255, unique=True)
    text = models.TextField(verbose_name=u'Block content', blank=True, null=True)
    template = models.CharField(max_length=255, blank=True, null=True)
    order = models.PositiveIntegerField(verbose_name=u'order', default=0)
    side = models.PositiveIntegerField(u'side', choices=SIDE_CHOICES, default=1)
    active = models.BooleanField(u'active', default=False)
    
    def __unicode__(self):
        return self.name
        
    class Meta:
        verbose_name = u'side block'
        verbose_name_plural = u'side blocks'
        ordering = ['active', 'order', 'name']


    class Admin:
        list_display = ('name', 'active', 'order',)
        search_fields = ('name', 'text')
