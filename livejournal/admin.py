from livejournal.models import LiveJournalPost
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

class LiveJournalPost_Inline(admin.StackedInline):
    model = LiveJournalPost
    extra = 1

class LiveJournalPostOptions(admin.ModelAdmin):
    list_display = ('post', 'need_crosspost')

# class PostOptions(admin.ModelAdmin):
#     inlines = [LiveJournalPost_Inline]

admin.site.register(LiveJournalPost, LiveJournalPostOptions)

