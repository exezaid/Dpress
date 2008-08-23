from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from utils.helpers import get_object_or_none
from blog.models import Post
from livejournal.util import lj_crosspost, lj_delete

SCREEN_CHOICES = (
    ('A', _('All')),
    ('R', _('Anonymous only')),
    ('F', _('non-Friends')),
    ('N', _('None')),
)

ACCESS_LEVELS = (
    ('public', 'Public'),
    ('private', 'Private'),
)

EDIT_INLINE = settings.ENABLE_LJ_CROSSPOST and models.TABULAR or False

class LiveJournalPost(models.Model):
    post = models.ForeignKey(Post, editable=False, db_column='post_id', related_name='livejournalpost',
                             edit_inline=EDIT_INLINE, max_num_in_admin=1, num_in_admin=1, num_extra_on_change=1)
    lj_id = models.IntegerField(editable=False, blank=True, null=False)

    need_crosspost = models.BooleanField(_('Needs crossposting'), default=True, core=True)

    no_comments = models.BooleanField(_('Turn off comments'), default=False, core=True)
    screen_comments = models.CharField(_('Comments screening'), max_length=1, choices=SCREEN_CHOICES, blank=False, default='N', core=True)
    access_level = models.CharField(_('Access level'), max_length=10, choices=ACCESS_LEVELS, blank=False, default='public', core=True)

    class Admin:
        list_display = ('post', 'need_crosspost')

    def __unicode__(self):
        return u'%s' % self.post


def get_lj_object_link(post):
    lj = get_object_or_none(LiveJournalPost, post=post)
    if lj:
        return '<a href="../../livejournal/livejournalpost/%s/">edit</a>' % lj.pk
    else:
        return ''
get_lj_object_link.allow_tags = True

Post.add_to_class('lj_object', get_lj_object_link)


if settings.ENABLE_LJ_CROSSPOST:
#    Post._meta.admin.list_display += ('lj_object', )
    models.signals.pre_save.connect(lj_crosspost, sender=LiveJournalPost)
    models.signals.pre_delete.connect(lj_delete, sender=LiveJournalPost)

