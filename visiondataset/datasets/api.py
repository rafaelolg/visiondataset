#!/usr/bin/env python
# -*- coding: utf-8 -*-
from djangorestframework.resources import ModelResource
from djangorestframework.views import ListOrCreateModelView, InstanceModelView, View
from django.core.urlresolvers import reverse

from .models import Dataset, Datum, DatumAttachment


class DatumResource(ModelResource):
    fields = ('name', 'created','type', 'attachments', 'file')
    model = Datum

    def type(self, instance):
        return instance.dtype.slug

    def attachments(self, instance):
        return reverse('api_attachment_list', kwargs={'datum__dataset_id':instance.dataset.id, 'datum_id':instance.id})

    def file(self, instance):
        return reverse('api_datum_file', kwargs={'datum__dataset_id':instance.dataset.id, 'datum_id':instance.id})

class DatasetResource(ModelResource):
    fields = ('name', 'created', 'datums')
    model = Dataset

    def datums(self, instance):
        return reverse('api_datum_list', kwargs={'dataset_id':instance.id})


class DatumFileApiView(View):

    def get(self, request, datum_id, datum__dataset_id):
        print('datum='+datum_id)
        print('datset='+datum__dataset_id)
        from .views import datum_file
        return datum_file(request, pk=datum_id, dataset_id=datum__dataset_id)



class DatumAttachmentResource(ModelResource):
    fields = ('name', 'created')
    model = DatumAttachment

class DatasetsApiView(ListOrCreateModelView):
    """docstring for DatasetApiView"""
    resource = DatasetResource


class DatumsApiView(ListOrCreateModelView):
    """docstring for DatasetApiView"""
    resource = DatumResource

class DatumAttachmentsApiView(ListOrCreateModelView):
    """docstring for DatasetApiView"""
    resource = DatumAttachmentResource
# api.py
