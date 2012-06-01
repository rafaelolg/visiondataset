"""urlconf for the base application"""

from django.conf.urls.defaults import url, patterns
from views import DatasetList, DatasetCreate, DatasetDetail


urlpatterns = patterns('visiondataset.datasets.views',
        url(r'^$', DatasetList.as_view(), name='datasets_dataset_list'),
        url(r'^create/?$', DatasetCreate.as_view(), name='datasets_dataset_create'),
        url(r'^(?P<slug>[^/]+)/detail/?$', DatasetDetail.as_view(), name='datasets_dataset_detail'),
)
