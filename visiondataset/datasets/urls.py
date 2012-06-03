"""urlconf for the base application"""

from django.conf.urls.defaults import url, patterns
from views import DatasetList, DatasetCreate, DatasetDetail, \
        DatumDetail, datum_package_download


urlpatterns = patterns('visiondataset.datasets.views',
        url(r'^$', DatasetList.as_view(), name='datasets_dataset_list'),
        url(r'^create/?$', DatasetCreate.as_view(), name='datasets_dataset_create'),
        url(r'^(?P<slug>[^/]+)/detail/?$', DatasetDetail.as_view(), name='datasets_dataset_detail'),
        url(r'^datum/(?P<slug>[^/]+)/detail/?$', DatumDetail.as_view(), name='datasets_datum_detail'),
        url(r'^datum/(?P<slug>[^/]+)/package/?$', datum_package_download, name='datasets_datum_package'),
)
