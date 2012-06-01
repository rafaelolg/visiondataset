# Create your views here.
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect, HttpResponseForbidden
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from models import Dataset, Datum, DataType
from view_mixins import LoginRequiredMixin

class DatasetListView(LoginRequiredMixin, ListView):
    context_object_name = 'dataset_list'
    paginate_by = 6
    allow_empty = True

    def get_queryset(self):
        datasets = Dataset.objects.all()
        return datasets

    def get_context_data(self, **kwargs):
        context = super(DatasetListView, self).get_context_data(**kwargs)
        return context

@login_required
def dataset_view(request, slug):
    """ Default view for the root """
    dataset = Dataset.objects.get(slug=slug)
    if request.user.has_perm('view_dataset'):
        print 'asdasd'
    return HttpResponseForbidden()
