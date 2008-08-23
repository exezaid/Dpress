from geotagging.models import Continent, Country
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

class CountryOptions(admin.ModelAdmin):
    list_display = ('name', 'continent')
    list_filter = ['continent']
    prepopulated_fields = {'slug': ('name',)}

class ContinentOptions(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Country, CountryOptions)
admin.site.register(Continent, ContinentOptions)

