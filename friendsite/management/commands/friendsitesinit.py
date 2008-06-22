from django.core.management.base import NoArgsCommand

class Command(NoArgsCommand):
    help = "Init same friendsites (django, python, django-press, byteflow)."

    def handle_noargs(self, **options):
        from friendsite.models import FriendSite
        FriendSite.objects.get_or_create(name='Django',
                                         defaults={
                                                   'url':"http://www.djangoproject.com",
                                                   'small_icon':'/media/sites/django.ico'
                                                   })

        FriendSite.objects.get_or_create(name='Python',
                                         defaults={
                                                   'url':"http://www.python.org",
                                                   'small_icon':'/media/sites/python.ico'
                                                   })
