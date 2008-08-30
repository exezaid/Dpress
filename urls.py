# Custom patches
from blog.sitemaps import BlogSitemap
from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib.sitemaps import FlatPageSitemap
from django.http import HttpResponseServerError
from django.template.context import RequestContext, Context
from django.template.loader import render_to_string
from os.path import join, dirname
import discussion.mail
import utils.patches

admin.autodiscover()

def error500(request, template_name='500.html'):
    try:
        output = render_to_string(template_name, {}, RequestContext(request))
    except:
        output = "Critical error. Administrator was notified." 
    #render_to_string(template_name, {}, Context())
    return HttpResponseServerError(output)

handler500 = 'urls.error500'

sitemaps = {
    'blog': BlogSitemap,
    'flat': FlatPageSitemap,
    }

try:
    import urls_local
    urlpatterns = urls_local.urlpatterns
except ImportError:
    urlpatterns = patterns('',)

urlpatterns += patterns(
    '',
    url('^admin/(.*)', admin.site.root),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^video/', include('tube.urls')),
    url(r'^openid/', include('openidconsumer.urls')),
    url(r'^openidserver/', include('openidserver.urls')),
    url(r'^%s' % settings.BLOG_URLCONF_ROOT, include('blog.urls')),
    url(r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    url(r'^pingback/', include('pingback.urls')),
    url(r'^$', 'blog.views.process_root_request'),
    url(r'^photo/', include('photologue.urls')),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^robots.txt$', include('robots.urls')),
    url(r'^feeds/', include('feed.urls')),
    url(r'^xmlrpc/', include('xmlrpc.urls')),
    )

# static urls will be disabled in production mode,
# forcing user to configure httpd
if settings.DEBUG:
    urlpatterns += patterns(
        '',
        url(r'^media/(.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        url(r'^static/(.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
        url(r'^admin-media/(.*)$', 'django.views.static.serve', {'document_root': join(dirname(admin.__file__), 'media')}),
        )

if 'wpimport' in settings.INSTALLED_APPS:
    urlpatterns += patterns(
        '',
        url(r'^wpimport/', include('wpimport.urls')),
        )

if 'debug' in settings.INSTALLED_APPS:
    urlpatterns += patterns(
        '',
        url('', include('debug.urls')),
        )
