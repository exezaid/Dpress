from django.conf.urls.defaults import *

#feed
from diario.feeds import RssEntriesFeed, AtomEntriesFeed

entries_feeds = {
    'rss': RssEntriesFeed,
    'atom': AtomEntriesFeed,
}


#feed by tag
from diario.feeds import RssEntriesByTagFeed, AtomEntriesByTagFeed

entries_by_tag_feeds = {
    'rss': RssEntriesByTagFeed,
    'atom': AtomEntriesByTagFeed,
}

#feed with comment
from diario.feeds import RssFreeCommentsFeed as RssWeblogCommentsFeed
from diario.feeds import AtomFreeCommentsFeed as AtomWeblogCommentsFeed
blog_comments_feeds = {
    'rss': RssWeblogCommentsFeed,
    'atom': AtomWeblogCommentsFeed,
}

#sitemap
from diario.sitemaps import DiarioSitemap

sitemaps = {
    'weblog': DiarioSitemap,
}

urlpatterns = patterns('',
     # homepage
     (r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'flatfiles/homepage.html'}),
     (r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),

     # weblog
     (r'^blog/(?P<url>(rss|atom))/$', 'django.contrib.syndication.views.feed', {'feed_dict': entries_feeds}),
     (r'^blog/tag/', include('diario.urls.tagged')),
     (r'^blog/tag/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': entries_by_tag_feeds}),
     (r'^blog/tag/(?P<tag>[^/]+)/(?P<slug>(rss|atom))/$', 'diario.views.syndication.feed', {'feed_dict': entries_by_tag_feeds}),
     (r'^blog/comments/(?P<url>(rss|atom))/$', 'django.contrib.syndication.views.feed', {'feed_dict': blog_comments_feeds}),
     (r'^blog/', include('diario.urls.entries')),

     # Uncomment this for admin:
     (r'^admin/', include('django.contrib.admin.urls')),
)
