from django_evolution.mutations import *
from django.db import models

MUTATIONS = [
    ChangeField('Post', 'language', initial=None, null=True)
]
