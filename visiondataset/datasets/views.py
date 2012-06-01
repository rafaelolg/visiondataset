# Create your views here.
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect, HttpResponseForbidden
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from guardian.shortcuts import get_objects_for_user, get_users_with_perms

from models import Dataset, Datum, DataType
from view_mixins import LoginRequiredMixin

class DatasetList(LoginRequiredMixin, ListView):
    context_object_name = 'dataset_list'
    paginate_by = 6
    allow_empty = True

    def get_queryset(self):
        datasets = get_objects_for_user(self.request.user, 'colaborate_dataset', klass=Dataset)
        return datasets

    def get_context_data(self, **kwargs):
        context = super(DatasetList, self).get_context_data(**kwargs)
        return context

class DatasetCreate(CreateView):
    pass


class DatasetDetail(LoginRequiredMixin, DetailView):
    context_object_name = "dataset"
    def get_queryset(self):
        datasets = get_objects_for_user(self.request.user, 'colaborate_dataset', klass=Dataset)
        return datasets
    success_url = 'datasets_dataset_list'
