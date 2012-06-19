#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render_to_response, redirect


from djangorestframework.resources import ModelResource
from djangorestframework.views import ListOrCreateModelView, InstanceModelView, ListModelView, View
from djangorestframework.permissions import IsAuthenticated, _403_FORBIDDEN_RESPONSE
from guardian.shortcuts import get_objects_for_user, get_users_with_perms,\
        assign, remove_perm

from sendfile import sendfile

from .models import Dataset, Datum, DatumAttachment
from .forms import DatumAttachmentForm
##################
#Resources

class DatumResource(ModelResource):
    fields = ('name', 'created','type', 'attachments', 'file')
    model = Datum
    queryset = Datum.objects.select_related('dataset', 'dtype')

    def type(self, instance):
        return instance.dtype.slug

    def file(self, instance):
        return reverse('api_datum_file',
                kwargs={'id':instance.id})

    def attachments(self, instance):
        return reverse('api_attachment_list',
                kwargs={'datum':instance.id})


class DatasetResource(ModelResource):
    fields = ('name', 'created', 'datums')
    model = Dataset

    def datums(self, instance):
        return reverse('api_datum_list', kwargs={'dataset':instance.id})


class DatumAttachmentResource(ModelResource):
    fields = ('name', 'created', 'file')
    model = DatumAttachment
    queryset = DatumAttachment.objects.select_related('datum')

    def file(self, instance):
        return reverse('api_attachment_file',
                kwargs={'id': instance.id})


###############
#Permissions

class DatasetPermission(IsAuthenticated):
    """
    Checks if a user has permissions to view the dataset of this view.
    """

    def check_permission(self, user):
        print('view.kwargs=')
        print(self.view.kwargs)
        dataset = self.view.get_dataset()
        super(DatasetPermission, self).check_permission(user)
        if not dataset.is_user_allowed(user):
            raise _403_FORBIDDEN_RESPONSE

######################
#VIEWS

class DatumFileApiView(View):
    permissions = (DatasetPermission,)

    def get_dataset(self):
        self._datum = get_object_or_404(Datum, **self.kwargs)
        dataset = self._datum.dataset
        return dataset

    def get(self, request, id):
        if not self._datum:
            self._datum = get_object_or_404(Datum, **self.kwargs)
        return sendfile(request, self._datum.package.path,
                attachment_filename=self._datum.file_name(), attachment=True)



class DatasetsApiView(ListModelView):
    """List Datasets for the current user"""
    resource = DatasetResource
    permissions = (IsAuthenticated,)

    def get_queryset(self):
        queryset = get_objects_for_user(self.user, 'dataset_colaborate' , klass=Dataset)
        return queryset


class DatumsApiView(ListModelView):
    """List the datums for the given dataset"""
    resource = DatumResource
    permissions = (DatasetPermission,)


    def get_dataset(self):
        dataset = get_object_or_404(Dataset, pk=self.kwargs['dataset'])
        return dataset


class DatumAttachmentsApiView(ListOrCreateModelView):
    """List and post new Attachments for the given datum of given dataset"""
    resource = DatumAttachmentResource
    permissions = (DatasetPermission,)
    form = DatumAttachmentForm

    def get_dataset(self):
        datum = get_object_or_404(Datum,
                pk=self.kwargs['datum'])
        dataset = datum.dataset
        return dataset

    def get_instance_data(self, model, content, **kwargs):
        data = super(DatumAttachmentsApiView, self).get_instance_data(model, content, **kwargs)
        data['owner'] = self.user
        data['original_name'] = data['package'].name
        return data

class DatumAttachmentFileApiView(View):
    permissions = (DatasetPermission,)

    def get_dataset(self):
        attachment = get_object_or_404(DatumAttachment, pk=self.kwargs['id'])
        dataset = attachment.datum.dataset
        return dataset

    def get(self, request, id):
        attachment = get_object_or_404(DatumAttachment, pk=self.kwargs['id'])
        return sendfile(request, attachment.package.path,
                attachment_filename=attachment.original_name, attachment=True)

# api.py
