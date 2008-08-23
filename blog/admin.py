from blog.models import Language, Post
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

class PostOptions(admin.ModelAdmin):
    list_display = ('name', 'date', 'author', 'enable_comments', 'comments_open', 'is_draft', 'view_link', 'language')
    search_fieldsets = ('name', 'text')
    list_filter = ('date', )
    fieldsets = (
        (None, {'fields': ('author', ('name', 'slug'), 'tags', 'text', 'render_method', 'date', 'language', ('is_draft', 'enable_comments'))}),
        ('Featured post', {'classes': ('collapse',), 'fields': ('is_featured', 'teaser')}),
        )
    if settings.WYSIWYG_ENABLE:
        js = (
              settings.MEDIA_URL + 'js/jquery.js',
              settings.MEDIA_URL + 'js/wymeditor/jquery.wymeditor.pack.js',
              '/' + settings.BLOG_URLCONF_ROOT + 'wysiwyg_js/',
             )
    prepopulated_fields = {'slug': ('name', )}

class LanguageOptions(admin.ModelAdmin):
    list_display = ('name', 'small_icon')

admin.site.register(Post, PostOptions)
admin.site.register(Language, LanguageOptions)

