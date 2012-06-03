# Create your views here.
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect, HttpResponseForbidden
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, DetailView, CreateView, \
        UpdateView, DeleteView
from django.shortcuts import get_object_or_404
from guardian.shortcuts import get_objects_for_user, get_users_with_perms
from guardian.shortcuts import assign
from django.core.exceptions import PermissionDenied

from models import Dataset, Datum, DataType
from view_mixins import LoginRequiredMixin, PermissionRequiredMixin
from forms import DatasetModelForm
from sendfile import sendfile



DATASET_COLABORATE_PERMISSION='dataset_colaborate'

class DatasetList(LoginRequiredMixin, ListView):
    context_object_name = 'dataset_list'
    paginate_by = 6
    allow_empty = True

    def get_queryset(self):
        datasets = get_objects_for_user(self.request.user, DATASET_COLABORATE_PERMISSION, klass=Dataset)
        return datasets

    def get_context_data(self, **kwargs):
        context = super(DatasetList, self).get_context_data(**kwargs)
        return context

class DatasetCreate(LoginRequiredMixin,  CreateView):
    model  = Dataset
    form_class = DatasetModelForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        assign(DATASET_COLABORATE_PERMISSION,self.request.user, self.object)
        return HttpResponseRedirect(self.get_success_url())


class DatasetDetail(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    context_object_name = "datum_list"
    paginate_by = 12
    allow_empty = True
    permission_required = DATASET_COLABORATE_PERMISSION
    raise_exception = True

    def get_object(self):
        if not hasattr(self,'dataset'):
            self.dataset = get_object_or_404(Dataset, pk=self.kwargs['pk'])
        return self.dataset

    def get_queryset(self):
        return Datum.objects.filter(dataset=self.get_object())

    def get_context_data(self, **kwargs):
        context = super(DatasetDetail, self).get_context_data(**kwargs)
        context['dataset'] = self.get_object()
        return context

class DatumDetail(LoginRequiredMixin, DetailView):
    context_object_name = "datum"
    model=Datum


@login_required
def datum_file(request, pk):
    datum = get_object_or_404(Datum, pk=pk)
    if datum.is_user_allowed(request.user):
        return sendfile(request, datum.package.path)
    else:
        return HttpResponseForbidden(_("You can't view this"));
