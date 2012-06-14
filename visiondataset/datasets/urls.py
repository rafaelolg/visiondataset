"""urlconf for the base application"""

from django.conf.urls.defaults import url, patterns
from views import DatasetList, DatasetCreate, DatasetDetail, \
        DatumDetail, DatumCreate, datum_file,datum_thumbnail, edit_colaborators,\
        remove_colaborators, dataset_as_zip, DatumAttachmentDetail,\
        datum_attachment_file, DatumAttachmentCreate


urlpatterns = patterns('visiondataset.datasets.views',
        url(r'^$', DatasetList.as_view(), name='datasets_dataset_list'),
        url(r'^create/?$', DatasetCreate.as_view(), name='datasets_dataset_create'),
        url(r'^(?P<pk>\d+)/?$', DatasetDetail.as_view(), name='datasets_dataset_detail'),
        url(r'^(?P<pk>\d+)/zip/?$', dataset_as_zip, name='datasets_dataset_zip'),
        url(r'^(?P<dataset_id>\d+)/colaborators/?$', edit_colaborators, name='datasets_dataset_colaborators'),
        url(r'^(?P<dataset_id>\d+)/colaborators/(?P<colaborator_id>\d+)/remove/?$',
            remove_colaborators, name='datasets_dataset_colaborators_remove'),
        url(r'^(?P<dataset_id>\d+)/datum/(?P<pk>\d+)/?$', DatumDetail.as_view(), name='datasets_datum_detail'),
        url(r'^(?P<dataset_id>\d+)/datum/create/?$', DatumCreate.as_view(), name='datasets_datum_create'),
        url(r'^(?P<dataset_id>\d+)/datum/(?P<pk>\d+)/file/?$', datum_file, name='datasets_datum_file'),
        url(r'^(?P<dataset_id>\d+)/datum/(?P<pk>\d+)/thumbnail/?$', datum_thumbnail, name='datasets_datum_thumbnail'),
        #TODO:
        url(r'^(?P<dataset_id>\d+)/datum/(?P<datum_id>\d+)/attachment/(?P<pk>\d+)/?$',
            DatumAttachmentDetail.as_view(), name='datasets_datumattachment_detail'),
        url(r'^(?P<dataset_id>\d+)/datum/(?P<datum_id>\d+)/attachment/(?P<pk>\d+)/file/?$',
            datum_attachment_file, name='datasets_datumattachment_file'),
        url(r'^(?P<dataset_id>\d+)/datum/(?P<datum_id>\d+)/attachment/create/?$',
            DatumAttachmentCreate.as_view(), name='datasets_datumattachment_create'),
)
