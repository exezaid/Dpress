from django.conf import settings
from django.dispatch import dispatcher
from django.db.models import signals
import photologue.models as models 
from photologue.models import PhotoEffect, PhotoSize  
# pylint: disable-msg=E1003,E1101

def init_data():
    pe, c = PhotoEffect.objects.get_or_create(name = 'Enhance Thumbnail')
    if c:
        pe.contrast = 1.2
        pe.sharpness = 1.3
        pe.save()
    
    ps, c = PhotoSize.objects.get_or_create(name = 'admin_thumbnail', 
                                            defaults={'width':100, 
                                                      'height':75,
                                                      'quality':70,
                                                      'crop':True,
                                                      'pre_cache':True,
                                                      })
    if c:
        ps.effect = pe

    ps, c = PhotoSize.objects.get_or_create(name = 'thumbnail',
                                            defaults={'width':100, 
                                                      'height':75,
                                                      'quality':70,
                                                      'crop':True,
                                                      'pre_cache':True,
                                                      })
    if c:
        ps.effect = pe

    ps, c = PhotoSize.objects.get_or_create(name = 'display',
                                            defaults={'width':400, 
                                                      'height':0,
                                                      'quality':70,
                                                      'crop':True,
                                                      'pre_cache':True,
                                                      })


dispatcher.connect(init_data, sender=models, signal=signals.post_syncdb)
