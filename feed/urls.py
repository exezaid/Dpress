from django.conf.urls.defaults import *
from django.contrib.syndication.views import feed

from feed.blog_feeds import AtomBlogEntries, RssBlogEntries, AtomCommentEntries, RssCommentEntries,\
     AtomPostsByTag, RssPostsByTag, AtomFeaturedBlogEntries, RssFeaturedBlogEntries

# Be careful, names of this keys are also used in templates and in feeds.py!
atom_feeds = {
    'blog': AtomBlogEntries,
    'comments': AtomCommentEntries,
    'tag': AtomPostsByTag,
    'featured': AtomFeaturedBlogEntries,
    }

rss_feeds = {
    'blog': RssBlogEntries,
    'comments': RssCommentEntries,
    'tag': RssPostsByTag,
    'featured': RssFeaturedBlogEntries,
    }

urlpatterns = patterns(
    '',
    url(r'^rss/(?P<url>.*)/$', feed, {'feed_dict': rss_feeds}, name="rss_feed"),
    url(r'^(?P<url>.*)/$', feed, {'feed_dict': atom_feeds}, name="atom_feed"),
)
