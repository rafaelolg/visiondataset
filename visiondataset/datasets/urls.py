"""urlconf for the base application"""

from django.conf.urls.defaults import url, patterns
from views import DatasetList, DatasetCreate, DatasetDetail, \
        DatumDetail, DatumCreate, datum_file,datum_thumbnail, edit_colaborators, remove_colaborators


urlpatterns = patterns('visiondataset.datasets.views',
        url(r'^$', DatasetList.as_view(), name='datasets_dataset_list'),
        url(r'^create/?$', DatasetCreate.as_view(), name='datasets_dataset_create'),
        url(r'^(?P<pk>\d+)/?$', DatasetDetail.as_view(), name='datasets_dataset_detail'),
        url(r'^(?P<dataset_id>\d+)/colaborators/?$', edit_colaborators, name='datasets_dataset_colaborators'),
        url(r'^(?P<dataset_id>\d+)/colaborators/(?P<colaborator_id>\d+)/remove/?$',
            remove_colaborators, name='datasets_dataset_colaborators_remove'),
        url(r'^(?P<dataset_id>\d+)/datum/(?P<pk>\d+)/?$', DatumDetail.as_view(), name='datasets_datum_detail'),
        url(r'^(?P<dataset_id>\d+)/datum/create/?$', DatumCreate.as_view(), name='datasets_datum_create'),
        url(r'^(?P<dataset_id>\d+)/datum/(?P<pk>\d+)/file/?$', datum_file, name='datasets_datum_file'),
        url(r'^(?P<dataset_id>\d+)/datum/(?P<pk>\d+)/thumbnail/?$', datum_thumbnail, name='datasets_datum_thumbnail'),
)
