#!/usr/bin/env python
# -*- coding: utf-8 -*-
from djangorestframework.resources import ModelResource
from djangorestframework.views import ListOrCreateModelView, InstanceModelView, View
from djangorestframework.mixins import ListModelMixin
from djangorestframework.permissions import IsAuthenticated
from django.core.urlresolvers import reverse

from .models import Dataset, Datum, DatumAttachment

from guardian.shortcuts import get_objects_for_user, get_users_with_perms,\
        assign, remove_perm

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
    permissions = (IsAuthenticated,)
    model = DatumAttachment


class DatasetsApiView(ListOrCreateModelView):
    """List Datasets for the current user"""
    resource = DatasetResource
    permissions = (IsAuthenticated,)

    def get_queryset(self):
        queryset = get_objects_for_user(self.request.user, 'dataset_colaborate' , klass=Dataset)
        return queryset

    def get(self, request, *args, **kwargs):
        import ipdb;ipdb.set_trace()
        return super(DatasetsApiView, self).get(request, *args, **kwargs)


class DatumsApiView(ListOrCreateModelView):
    """List the datums for the given dataset"""
    resource = DatumResource
    permissions = (IsAuthenticated,)


class DatumAttachmentsApiView(ListOrCreateModelView):
    """List and post new Attachments for the given datum of given dataset"""
    resource = DatumAttachmentResource
    permissions = (IsAuthenticated,)

# api.py
