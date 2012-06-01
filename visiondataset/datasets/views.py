# Create your views here.
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect, HttpResponseForbidden
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404
from guardian.shortcuts import get_objects_for_user, get_users_with_perms

from models import Dataset, Datum, DataType
from view_mixins import LoginRequiredMixin, PermissionRequiredMixin

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

class DatasetCreate(CreateView):
    pass


class DatasetDetail(ListView):
    context_object_name = "datum_list"
    paginate_by = 12
    allow_empty = True

    def get_queryset(self):
        self.dataset = get_object_or_404(Dataset, slug=self.kwargs['slug'])
        return Datum.objects.filter(dataset=self.dataset)

    def get_context_data(self, **kwargs):
        context = super(DatasetDetail, self).get_context_data(**kwargs)
        context['dataset'] = self.dataset
        import ipdb;ipdb.set_trace()
        return context

