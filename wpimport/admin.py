from wpimport.models import Category, Comment, Post, User
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(User)
admin.site.register(Post)

