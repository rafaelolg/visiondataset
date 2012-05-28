from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

class Dataset(models.Model):
    """Set of datums"""
    creation_time = models.TimeField(auto_now_add=True)
    name = models.CharField(max_length=256, blank=False)
    owner = models.ForeignKey(User, null=False)
    class Meta:
        permissions = (
            ('view_dataset', _('View Dataset')),
            ('add_datum_dataset', _('Add elements')),
        )
        get_latest_by = 'creation_time'
    def __unicode__(self):
        return self.name



class DataType(models.Model):
    """docstring"""
    slug = models.SlugField(max_length=50, blank=True)
    @models.permalink
    def get_absolute_url(self):
        return ('datatype_view',(),{'slug':str(self.slug)})
    def __unicode__(self):
        return self.slug


class Datum(models.Model):
    """Data element"""
    dataset = models.ForeignKey(Dataset, null=False)
    owner = models.ForeignKey(User, null=False)
    creation_time = models.TimeField(auto_now_add=True)
    name = models.CharField(max_length=256, blank=False)
    description = models.TextField(blank=True)
    package = models.FileField(upload_to='datum', max_length=100)
    dtype = models.ForeignKey(DataType)
    class Meta:
        permissions = (
            ('view_datum', _('View Element Datum')),
        )
        get_latest_by = 'creation_time'
    def __unicode__(self):
        self.name

