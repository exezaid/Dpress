from datetime import datetime as dt

from django.contrib.sitemaps import Sitemap

from blog.models import Post

class BlogSitemap(Sitemap):
    changefreq = "never"
    priority = 0.8

    def items(self):
        return Post.objects.exclude(date__gt=dt.now())

    def lastmod(self, obj):
        return obj.date
