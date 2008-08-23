from django.db.models import signals
from django.conf import settings
from blog import models 
from blog.models import Language

# pylint: disable-msg=E1003,E1101
#
def init_data(**kwargs):
    LANGS = [
             {"small_icon": "\/media\/flags\/us.gif", "name": "English"},
             {"small_icon": "\/media\/flags\/it.gif", "name": "Italiano"}, 
             ]
    for data in LANGS:
        Language.objects.get_or_create(name=data['name'], 
                                       defaults={'small_icon':data['small_icon']})

signals.post_syncdb.connect(init_data, sender=models)
