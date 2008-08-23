from accounts.models import ActionRecord
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

class ActionRecordOptions(admin.ModelAdmin):
    list_display = ('user', 'date')
    search_fieldsets = ('user')
    list_filter = ('user', 'date')

admin.site.register(ActionRecord, ActionRecordOptions)

