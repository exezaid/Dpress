from django.conf.urls.defaults import *

from openidserver.views import endpoint, accept

urlpatterns = patterns(
    '',
    url(r'^$', endpoint, name="openid_endpoint"),
    url(r'accept/$', accept, name="openid_accept"),
)
