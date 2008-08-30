from django.db import models

class FriendSite(models.Model):
    name = models.CharField(max_length=30)
    url = models.URLField()
    small_icon = models.ImageField(null=True, blank=True,upload_to='sites')

    class Admin:
        list_display = ('name', 'url', 'small_icon')

    def __unicode__(self):
        return self.name
