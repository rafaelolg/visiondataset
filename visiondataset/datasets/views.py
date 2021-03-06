#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseRedirect, HttpResponseForbidden, \
    HttpResponse
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, DetailView, \
        CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.core.exceptions import PermissionDenied
from django.template import RequestContext
from guardian.shortcuts import get_objects_for_user, get_users_with_perms, \
    assign, remove_perm
from django.contrib import messages
from django.template.defaultfilters import slugify

from sendfile import sendfile

from models import Dataset, Datum, DataType, DatumAttachment
from visiondataset.base.view_mixins import LoginRequiredMixin, \
    PermissionRequiredMixin
from forms import DatasetModelForm, DatumModelForm, ColaboratorForm, \
    DatumAttachmentForm
from util import base_name

DATASET_COLABORATE_PERMISSION = 'dataset_colaborate'


##################DETAIL AND LISDT
class DatasetList(LoginRequiredMixin, ListView):

    context_object_name = 'dataset_list'
    paginate_by = 6
    allow_empty = True

    def get_queryset(self):
        datasets = get_objects_for_user(self.request.user,
                                        DATASET_COLABORATE_PERMISSION,
                                        klass=Dataset)
        return datasets


class DatasetDetail(PermissionRequiredMixin, LoginRequiredMixin, ListView):

    context_object_name = 'datum_list'
    paginate_by = 12
    allow_empty = True
    permission_required = DATASET_COLABORATE_PERMISSION
    raise_exception = True

    def get_object(self):
        if not hasattr(self, 'dataset'):
            self.dataset = get_object_or_404(Dataset, pk=self.kwargs['pk'])
        return self.dataset

    def get_queryset(self):
        return Datum.objects.filter(dataset=self.get_object())

    def get_context_data(self, **kwargs):
        context = super(DatasetDetail, self).get_context_data(**kwargs)
        context['dataset'] = self.get_object()

        context['next'] = self.get_object().get_absolute_url()
        return context


class DatumDetail(LoginRequiredMixin, DetailView):

    context_object_name = 'datum'
    model = Datum

    def dispatch(self, request, *args, **kwargs):
        self.kwargs = kwargs
        self.args = args
        datum = self.get_object()
        if datum.is_user_allowed(request.user):
            return super(DatumDetail, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden(_("You can't view this"))

    def get_context_data(self, **kwargs):
        context = super(DatumDetail, self).get_context_data(**kwargs)
        context['attachments'] = self.object.datumattachment_set.all()

        context['next'] = self.object.get_absolute_url()
        return context


class DatumAttachmentDetail(LoginRequiredMixin, DetailView):

    context_object_name = 'attachment'
    model = DatumAttachment

    def dispatch(self, request, *args, **kwargs):
        self.kwargs = kwargs
        self.args = args
        datum = get_object_or_404(Datum, pk=kwargs['datum_id'])
        if datum.is_user_allowed(request.user):
            return super(DatumAttachmentDetail, self).dispatch(request, *args,
                    **kwargs)
        else:
            return HttpResponseForbidden(_("You can't view this"))

    def get_context_data(self, **kwargs):
        context = super(DatumAttachmentDetail, self).get_context_data(**kwargs)
        context['dataset_id'] = self.kwargs['dataset_id']
        context['datum_id'] = self.kwargs['datum_id']

        context['next'] = self.object.get_absolute_url()
        return context


################ GET FILES
@login_required
def datum_attachment_file(request, pk, datum_id=None, dataset_id=None):
    datum = get_object_or_404(Datum, pk=datum_id)
    attachment = get_object_or_404(DatumAttachment, pk=pk)
    filename = attachment.original_name
    absolut_file_path = attachment.package.path
    return datum_send_file(request, filename, absolut_file_path, datum)


@login_required
def datum_file(request, pk, dataset_id=None):
    datum = get_object_or_404(Datum, pk=pk)
    filename = datum.file_name()
    absolut_file_path = datum.package.path
    return datum_send_file(request, filename, absolut_file_path, datum)


@login_required
def datum_thumbnail(request, pk, dataset_id=None):
    datum = get_object_or_404(Datum, pk=pk)
    filename = 'thumb_' + datum.file_name()
    absolut_file_path = datum.get_thumbnail_file_path()
    return datum_send_file(request, filename, absolut_file_path, datum)


@login_required
def datum_send_file(request, filename, absolut_file_path, datum,):
    if datum.is_user_allowed(request.user):
        return sendfile(request, absolut_file_path, attachment=True,
                        attachment_filename=filename)
    else:
        return HttpResponseForbidden(_("You can't view this"))


@login_required
def dataset_as_zip(request, pk):
    dataset = get_object_or_404(Dataset, pk=pk)
    if not request.user.has_perm('dataset_colaborate', dataset):
        return HttpResponseForbidden(_("You can't view this"))
    response = HttpResponse(mimetype='application/zip')
    response['Content-Disposition'] = 'attachment; filename=%s.zip'\
         % slugify(dataset.name)
    response.write(dataset.to_zip().read())
    return response


####################CREATE
class DatasetCreate(LoginRequiredMixin, CreateView):

    model = Dataset
    form_class = DatasetModelForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        assign(DATASET_COLABORATE_PERMISSION, self.request.user, self.object)
        return HttpResponseRedirect(self.get_success_url())


class DatumCreate(LoginRequiredMixin, CreateView):

    model = Datum
    form_class = DatumModelForm

    def dispatch(self, request, *args, **kwargs):
        self.kwargs = kwargs
        self.args = args
        dataset = get_object_or_404(Dataset, pk=kwargs['dataset_id'])
        if dataset.is_user_allowed(request.user):
            return super(DatumCreate, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden(_("You can't view this"))

    def get_context_data(self, **kwargs):
        context = super(DatumCreate, self).get_context_data(**kwargs)
        context['dataset_id'] = self.kwargs['dataset_id']
        return context

    def form_valid(self, form):
        dtype = form.cleaned_data['dtype']
        if form.cleaned_data['package'].content_type in ('application/zip',
                'application/x-zip'):
            if not dtype.is_acceptable(form.cleaned_data['package'].name):
                return self.process_zip(form)
        if dtype.is_acceptable(form.cleaned_data['package'].name):
            self.object = form.save(commit=False)
            self.object.dataset_id = self.kwargs['dataset_id']
            self.object.owner = self.request.user
            self.object.name = self.object.package.name
            self.object.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            messages.error(self.request, _('Invalid file type: ')
                            + form.cleaned_data['package'].content_type)
            return self.form_invalid(form)

    def process_zip(self, form):
        zfile = form.cleaned_data['package']
        dataset = get_object_or_404(Dataset, pk=self.kwargs['dataset_id'])
        owner = self.request.user
        dtype = form.cleaned_data['dtype']
        dataset.add_from_zip(zfile, dtype, owner)
        return HttpResponseRedirect(dataset.get_absolute_url())


class DatumAttachmentCreate(LoginRequiredMixin, CreateView):

    model = DatumAttachment
    form_class = DatumAttachmentForm

    def dispatch(self, request, *args, **kwargs):
        datum = get_object_or_404(Datum, pk=kwargs['datum_id'])
        if datum.is_user_allowed(request.user):
            return super(DatumAttachmentCreate, self).dispatch(request, *args,
                    **kwargs)
        else:
            return HttpResponseForbidden(_("You can't view this"))

    def get_context_data(self, **kwargs):
        context = super(DatumAttachmentCreate, self).get_context_data(**kwargs)
        context['dataset_id'] = self.kwargs['dataset_id']
        context['datum_id'] = self.kwargs['datum_id']
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.datum_id = self.kwargs['datum_id']
        self.object.owner = self.request.user
        self.object.original_name = self.object.package.name
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


##################DELETE
@login_required
def remove_colaborators(request, dataset_id, colaborator_id):
    dataset = get_object_or_404(Dataset, pk=dataset_id)
    if request.user != dataset.owner or colaborator_id == dataset.owner_id:
        return HttpResponseForbidden(_("You can't view this"))
    colaborator = get_object_or_404(User, pk=colaborator_id)
    remove_perm(DATASET_COLABORATE_PERMISSION, colaborator, dataset)
    messages.success(request, _('Removed: ') + colaborator.username)
    return redirect('datasets_dataset_colaborators', dataset_id=dataset_id)


class DatumAttachmentDelete(DeleteView):
    model = DatumAttachment

    def dispatch(self, request, *args, **kwargs):
        attachment = get_object_or_404(DatumAttachment, pk=kwargs.get('pk'))
        datum = get_object_or_404(Datum, pk=kwargs.get('datum_id'))
        self.success_url = datum.get_absolute_url()
        if not datum.is_user_allowed(request.user):
            return HttpResponseForbidden(_("You can't do this"))
        return super(DatumAttachmentDelete, self).dispatch(request, *args,
                **kwargs)

##################EDIT
@login_required
def edit_colaborators(request, dataset_id):
    dataset = get_object_or_404(Dataset, pk=dataset_id)
    if request.user != dataset.owner and (not request.user.is_staff):
        return HttpResponseForbidden(_("You can't view this"))
    if request.method == 'POST':
        form = ColaboratorForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            try:
                u = User.objects.get(username=username)
            except Exception, e:
                messages.error(request, _('No such user: ') + username)
            assign(DATASET_COLABORATE_PERMISSION, u, dataset)
            form = ColaboratorForm()
            messages.success(request, _('New colaborator: ') + username)
    else:
        form = ColaboratorForm()
    return render_to_response('datasets/dataset_colaborators.html',
            {'form': form, 'dataset': dataset},
            context_instance=RequestContext(request))
    return HttpResponseForbidden()
