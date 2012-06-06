"""urlconf for the base application"""

from django.conf.urls.defaults import url, patterns


urlpatterns = patterns('visiondataset.base.views',
    url(r'^$', 'home', name='home'),
    url(r'^autocomplete-users/$', 'autocomplete_users', name='autocomplete_users'),
)
