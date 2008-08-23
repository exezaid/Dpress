from pingback.models import Pingback, PingbackClient, DirectoryPing
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

class DirectoryPingOptions(admin.ModelAdmin):
    list_display = ['url', 'date', 'success']

class PingbackClientOptions(admin.ModelAdmin):
    list_display = ('admin_object', 'url', 'date', 'success')

class PingbackOptions(admin.ModelAdmin):
    list_display = ('url', 'admin_object', 'date', 'approved', 'title')

admin.site.register(DirectoryPing, DirectoryPingOptions)
admin.site.register(PingbackClient, PingbackClientOptions)
admin.site.register(Pingback, PingbackOptions)

