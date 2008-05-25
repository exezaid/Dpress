from datetime import datetime as dt

from django.contrib.syndication.feeds import Feed as RssFeed
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.template.defaultfilters import pluralize

from atom import Feed as AtomFeed

from blog.models import Post
from discussion.models import CommentNode
from utils.helpers import reverse
from tagging.models import Tag, TaggedItem
from tagging.utils import get_tag_list


def link(location):
    return '%s://%s%s' % (settings.SITE_PROTOCOL, Site.objects.get_current().domain, location)


def _BlogEntries(Feed, type='atom'):
    class BlogEntries(Feed):
        def feed_id(self):
            return link(reverse('post_list'))
        link = feed_id

        feed_title = u"%s blog posts" % Site.objects.get_current().name
        title = feed_title

        def feed_authors(self):
            return ({"name": user.name} for user in User.objects.filter(is_staff=True))

        def feed_links(self):
            return ({'rel': u'alternate', 'href': self.feed_id()},
                    {'rel': u'self', 'href': link(reverse('%s_feed' % type, 'blog'))})

        def items(self):
            return Post.objects.exclude(date__gt=dt.now()).order_by('-date')[:5]

        def item_id(self, item):
            return link(item.get_absolute_url())

        def item_title(self, item):
            return 'html', item.name

        def item_updated(self, item):
            return item.upd_date

        def item_published(self, item):
            return item.date

        def item_content(self, item):
            html = settings.SHORT_POSTS_IN_FEED and item.html_short or item.html
            return {'type': 'html'}, html

        def item_categories(self, item):
            return ({'term': unicode(tag)} for tag in item.get_tags())

        def item_links(self, item):
            return ({'rel': u'self', 'href': self.item_id(item)},
                    {'rel': u'alternate', 'href': self.item_id(item)})
    return BlogEntries


def get_tags_bit(tags):
    return '+'.join([tag.name for tag in tags])


def _PostsByTag(Feed, type='atom'):
    class PostsByTag(Feed):
        def get_object(self, bits):
            if len(bits) != 1:
                raise ObjectDoesNotExist
            else:
                return get_tag_list(bits[0].split('+'))

        def feed_id(self, obj):
            if not obj:
                raise Http404
            return link(reverse('post_by_tag', tag=get_tags_bit(obj)))
        link = feed_id

        def feed_title(self, obj):
            site = Site.objects.get_current()
            return u"%s blog posts with tag%s %s" % (
                site.name,
                pluralize(len(obj)),
                ', '.join([tag.name for tag in obj]))
        title = feed_title

        def feed_authors(self):
            return ({"name": user.name} for user in User.objects.filter(is_staff=True))

        def feed_links(self, obj):
            return ({'rel': u'alternate', 'href': self.feed_id(obj)},
                    {'rel': u'self', 'href': link(reverse(
                            '%s_feed' % type,
                            'tag/%s' % get_tags_bit(obj)))})

        def items(self, obj):
            return TaggedItem.objects.get_union_by_model(Post, obj)[:5]

        def item_id(self, item):
            return link(item.get_absolute_url())

        def item_title(self, item):
            return 'html', item.name

        def item_updated(self, item):
            return item.upd_date

        def item_published(self, item):
            return item.date

        def item_content(self, item):
            html = settings.SHORT_POSTS_IN_FEED and item.html_short or item.html
            return {'type': 'html'}, html

        def item_links(self, item):
            return ({'rel': u'self', 'href': self.item_id(item)},
                    {'rel': u'alternate', 'href': self.item_id(item)})
    return PostsByTag


def _CommentEntries(Feed, type='atom'):
    class CommentEntries(Feed):
        # If feed get extra_params, then this will be comments for particular entry,
        # else - all comments
        def get_object(self, bits):
            if len(bits) > 1:
                raise ObjectDoesNotExist
            elif len(bits) == 1:
                return Post.objects.get(id=bits[0])
	    else:
                return None

        def feed_id(self, obj):
            if obj:
                return link(obj.get_absolute_url())
            else:
                return link('%s#comments' % reverse('post_list'))
        link = feed_id

        def feed_title(self, obj):
            site = Site.objects.get_current()
            if obj:
                return '%s blog comments on %s' % (site.name, obj.name)
            else:
                return '%s blog comments' % site.name
        title = feed_title

        def feed_authors(self, obj):
            if obj:
                return ({'name': c.user.name} for c in obj.comments.all())
            else:
                return ({'name': c.user.name} for c in self.items(obj))

        def feed_links(self, obj):
            return ({'rel': u'alternate', 'href': self.feed_id(obj)},
                    {'rel': u'self', 'href': link(reverse(
                            '%s_feed' % type,
                            'comments/%s' % str(getattr(obj, 'id', ''))))})

        def items(self, obj):
            if obj:
                return CommentNode.objects.for_object(obj).order_by('-pub_date')[:30]
            else:
                return CommentNode.objects.order_by('-pub_date')[:30]

        def item_id(self, item):
            return link(item.get_absolute_url())

        def item_title(self, item):
            return 'Comment on %s by %s' % (item.object.name, item.user.name)

        def item_updated(self, item):
            return item.upd_date

        def item_published(self, item):
            return item.pub_date

        def item_content(self, item):
            return {'type': 'html'}, item.body_html

        def item_links(self, item):
            return ({'rel': u'self', 'href': self.item_id(item)},
                    {'rel': u'alternate', 'href': self.item_id(item)})

        def item_authors(self, item):
            return ({'name': item.user.name}, )
    return CommentEntries


# Ok, time to build our feeds!
AtomBlogEntries = _BlogEntries(AtomFeed)
RssBlogEntries = _BlogEntries(RssFeed, 'rss')
AtomPostsByTag = _PostsByTag(AtomFeed)
RssPostsByTag = _PostsByTag(RssFeed, 'rss')
AtomCommentEntries = _CommentEntries(AtomFeed)
RssCommentEntries = _CommentEntries(RssFeed, 'rss')


# Featured posts feeds
# DRY violation, needs refactoring
class AtomFeaturedBlogEntries(AtomBlogEntries):
    def feed_updated(self):
        return Post.featured_objects.order_by('-date')[0].date

    def items(self):
        return Post.featured_objects.exclude(date__gt=dt.now()).order_by('-date')[:5]

class RssFeaturedBlogEntries(RssBlogEntries):
    def feed_updated(self):
        return Post.featured_objects.order_by('-date')[0].date

    def items(self):
        return Post.featured_objects.exclude(date__gt=dt.now()).order_by('-date')[:5]
