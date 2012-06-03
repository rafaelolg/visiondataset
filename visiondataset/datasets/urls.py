"""urlconf for the base application"""

from django.conf.urls.defaults import url, patterns
from views import DatasetList, DatasetCreate, DatasetDetail, \
        DatumDetail, datum_file


urlpatterns = patterns('visiondataset.datasets.views',
        url(r'^$', DatasetList.as_view(), name='datasets_dataset_list'),
        url(r'^create/?$', DatasetCreate.as_view(), name='datasets_dataset_create'),
        url(r'^(?P<pk>\d+)/?$', DatasetDetail.as_view(), name='datasets_dataset_detail'),
        url(r'^datum/(?P<pk>\d+)/?$', DatumDetail.as_view(), name='datasets_datum_detail'),
        url(r'^datum/(?P<pk>\d+)/file/?$', datum_file, name='datasets_datum_file'),
)
