import os
from django.core.management.base import NoArgsCommand
from optparse import make_option

class Command(NoArgsCommand):
    help = "Refresh the rendered html posts."

    def handle_noargs(self, **options):
        from blog.models import Post
        for post in Post.objects.all():
            post.save()
