from friendsite.models import FriendSite
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

class FriendSiteOptions(admin.ModelAdmin):
    list_display = ('name', 'url', 'small_icon')

admin.site.register(FriendSite, FriendSiteOptions)

