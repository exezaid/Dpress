from discussion.models import CommentNode
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

class CommentNodeOptions(admin.ModelAdmin):
    list_display = ('get_clean_html', 'user', 'pub_date', 'content_type', 'object_id', 'reply_to_id', 'approved')

admin.site.register(CommentNode, CommentNodeOptions)

