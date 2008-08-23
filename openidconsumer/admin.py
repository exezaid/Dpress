from openidconsumer.models import UserAssociation
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

class UserAssociationOptions(admin.ModelAdmin):
    list_display = ('openid_url', 'user')
    list_filter = ('user', )
    search_fieldsets = ('openid_url', 'user')

admin.site.register(UserAssociation, UserAssociationOptions)

