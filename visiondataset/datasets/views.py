# Create your views here.
from django.http import Http404, HttpResponseRedirect
from django.conf import settings
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils.translation import ugettext_lazy as _

from models import Dataset, Datum, DataType

class DatasetListView(ListView):
    context_object_name = 'dataset_list'
    paginate_by = 6
    allow_empty = True

    def get_queryset(self):
        datasets = Dataset.objects.all()
        return datasets

    def get_context_data(self, **kwargs):
        context = super(DatasetListView, self).get_context_data(**kwargs)
        return context
