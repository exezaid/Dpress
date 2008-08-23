from datetime import datetime, timedelta

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from utils.fields import AutoOneToOneField
from accounts.managers import RegistrationManager, ResetManager, EmailManager, ApprovalManager


## Monkey-patching User model
#User.add_to_class('site', models.URLField(verify_exists=False, blank=True))
#User.add_to_class('email_new', models.EmailField(blank=True))
#
#User._meta.admin.fields += (
#    ('Byteflow Extensions', {'fields': ('site', 'email_new')}),
#    )
#User._meta.admin.list_display = ('username', 'email', 'first_name', 'is_staff', 'is_active')
#User._meta.admin.search_fields = ('username', 'first_name', 'email')
class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True, db_index=True)
    site = models.URLField(verify_exists=False, blank=True, null=True)
    email_new = models.EmailField(blank=True)


def _get_name(self):
    return self.first_name

def _set_name(self, name):
    self.first_name = name

User.name = property(_get_name, _set_name)


ACTION_RECORD_TYPES = (('A', 'Activation'),
                       ('R', 'Password reset'),
                       ('E', 'Email change'),
                       ('C', 'Comment approve')
                       )

class ActionRecord(models.Model):
    """Record that holds activation_key generated upon user registration"""
    user = models.ForeignKey(User)
    action_key = models.CharField(max_length=40)
    date = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=1, choices=ACTION_RECORD_TYPES)

    objects = models.Manager()
    registrations = RegistrationManager()
    resets = ResetManager()
    emails = EmailManager()
    approvals = ApprovalManager()

    def __unicode__(self):
        return u"%s record for %s" % (self.get_type_display(), self.user.email)

    @property
    def expired(self):
        """
        Determines whether this Profile's activation key has expired,
        based on the value of the setting ``ACTION_RECORD_DAYS``.

        Set ``ACTION_RECORD_DAYS`` in 0 to disable expiring
        """
        if settings.ACTION_RECORD_DAYS:
            expiration_date = timedelta(days=settings.ACTION_RECORD_DAYS)
            return self.date + expiration_date <= datetime.now()
        else:
            return False

    class Admin:
        list_display = ('user', 'date')
        search_fields = ('user')
        list_filter = ('user', 'date')

    class Meta:
        db_table = 'actionrecord'
