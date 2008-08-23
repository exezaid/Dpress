from blogroll.models import Link
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

class LinkOptions(admin.ModelAdmin):
    list_display = ['name', 'url', 'relations', 'order']

admin.site.register(Link, LinkOptions)

