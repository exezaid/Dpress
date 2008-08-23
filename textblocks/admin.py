from textblocks.models import TextBlock, SideBlock
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

class TextBlockOptions(admin.ModelAdmin):
    list_display = ('code', 'name', 'comment',)
    search_fieldsets = ('name', 'text')

class SideBlockOptions(admin.ModelAdmin):
    list_display = ('name', 'active', 'order',)
    search_fieldsets = ('name', 'text')

admin.site.register(TextBlock, TextBlockOptions)
admin.site.register(SideBlock, SideBlockOptions)

