""" Default urlconf for visiondataset """
from django.conf import settings
from django.conf.urls.defaults import include, patterns
from django.contrib import admin
admin.autodiscover()

def bad(request):
    """ Simulates a server error """
    1 / 0

urlpatterns = patterns('',
    (r'', include('visiondataset.base.urls')),
    (r'^dataset/', include('visiondataset.datasets.urls')),
    #amdin
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    #3rd party
    (r'', include('debug_toolbar_user_panel.urls')),
    (r'^accounts/', include('userena.urls')),
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^bad/$', bad),
)

## In DEBUG mode, serve media files through Django.
if settings.DEBUG:
    # Remove leading and trailing slashes so the regex matches.
    media_url = settings.MEDIA_URL.lstrip('/').rstrip('/')
    urlpatterns += patterns('',
        (r'^%s/(?P<path>.*)$' % media_url, 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )
