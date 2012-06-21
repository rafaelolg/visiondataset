#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls.defaults import url, patterns
from views import DatasetList, DatasetCreate, DatasetDetail, DatumDetail, \
    DatumCreate, datum_file, datum_thumbnail, edit_colaborators, \
    remove_colaborators, dataset_as_zip, DatumAttachmentDetail, \
    datum_attachment_file, DatumAttachmentCreate

from api import DatasetsApiView, DatumsApiView, DatumAttachmentsApiView, \
    DatumFileApiView, DatumAttachmentFileApiView

urlpatterns = patterns(
    'visiondataset.datasets.views',
    url(r'^$', DatasetList.as_view(), name='datasets_dataset_list'),
    url(r'^create/?$', DatasetCreate.as_view(), name='datasets_dataset_create'),
    url(r'^(?P<pk>\d+)/?$', DatasetDetail.as_view(),
        name='datasets_dataset_detail'),
    url(r'^(?P<pk>\d+)/zip/?$', dataset_as_zip, name='datasets_dataset_zip'),
    url(r'^(?P<dataset_id>\d+)/colaborators/?$', edit_colaborators,
        name='datasets_dataset_colaborators'),
    url(r'^(?P<dataset_id>\d+)/colaborators/(?P<colaborator_id>\d+)/remove/?$',
        remove_colaborators, name='datasets_dataset_colaborators_remove'),
    url(r'^(?P<dataset_id>\d+)/datum/(?P<pk>\d+)/?$', DatumDetail.as_view(),
        name='datasets_datum_detail'),
    url(r'^(?P<dataset_id>\d+)/datum/create/?$', DatumCreate.as_view(),
        name='datasets_datum_create'),
    url(r'^(?P<dataset_id>\d+)/datum/(?P<pk>\d+)/file/?$', datum_file,
        name='datasets_datum_file'),
    url(r'^(?P<dataset_id>\d+)/datum/(?P<pk>\d+)/thumbnail/?$',
        datum_thumbnail, name='datasets_datum_thumbnail'),
    url(r'^(?P<dataset_id>\d+)/datum/(?P<datum_id>\d+)/attachment/(?P<pk>\d+)/?$',
        DatumAttachmentDetail.as_view(),
        name='datasets_datumattachment_detail'),
    url(r'^(?P<dataset_id>\d+)/datum/(?P<datum_id>\d+)/attachment/(?P<pk>\d+)/file/?$',
        datum_attachment_file, name='datasets_datumattachment_file'),
    url(r'^(?P<dataset_id>\d+)/datum/(?P<datum_id>\d+)/attachment/create/?$',
        DatumAttachmentCreate.as_view(), name='datasets_datumattachment_create'),
    url(r'^api/datasets/?$', DatasetsApiView.as_view(), name='api_dataset_list'),
    url(r'^api/datasets/(?P<dataset>\d+)/datums/?$', DatumsApiView.as_view(),
        name='api_datum_list'),
    url(r'^api/datums/(?P<id>\d+)/file/?$', DatumFileApiView.as_view(),
        name='api_datum_file'),
    url(r'^api/datums/(?P<datum>\d+)/attachments/?$',
        DatumAttachmentsApiView.as_view(), name='api_attachment_list'),
    url(r'^api/attachments/(?P<id>\d+)/file/?$',
        DatumAttachmentFileApiView.as_view(), name='api_attachment_file'),
    )
