"""urlconf for the base application"""

from django.conf.urls.defaults import url, patterns
from views import DatasetListView


urlpatterns = patterns('visiondataset.datasets.views',
        url(r'^$', DatasetListView.as_view(), name='dataset_list'),
)
