from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField, AutoSlugField


class Dataset(models.Model):
    """Set of datums"""
    name = models.CharField(max_length=256, blank=False)
    slug = AutoSlugField(_('slug'), populate_from='name')
    owner = models.ForeignKey(User, null=False)
    created = CreationDateTimeField(_('created'))
    class Meta:
        permissions = (
            ('view_dataset', _('View Dataset')),
            ('add_datum_dataset', _('Add elements')),
        )
        get_latest_by = 'created'
        ordering = ('-created',)
    @models.permalink
    def get_absolute_url(self):
        return ('dataset.views.datatype',(),{'slug':str(self.slug)})
    def __unicode__(self):
        return self.name



class DataType(models.Model):
    """docstring"""
    name = models.CharField(max_length=50, blank=False)
    slug = AutoSlugField(_('slug'), populate_from='name')
    @models.permalink
    def get_absolute_url(self):
        return ('dataset.views.datatype',(),{'slug':str(self.slug)})
    def __unicode__(self):
        return self.name


class Datum(models.Model):
    """Data element"""
    dataset = models.ForeignKey(Dataset, null=False)
    owner = models.ForeignKey(User, null=False)
    created = CreationDateTimeField(_('created'))
    name = models.CharField(max_length=256, blank=False)
    slug = AutoSlugField(_('slug'), populate_from='name')
    description = models.TextField(_('description'), blank=True, null=True)
    package = models.FileField(upload_to='datum', max_length=100)
    dtype = models.ForeignKey(DataType)
    class Meta:
        permissions = (
            ('view_datum', _('View Element Datum')),
        )
        get_latest_by = 'created'
        ordering = ('dataset','-created')
    @models.permalink
    def get_absolute_url(self):
        return ('dataset.views.datatype',(),{'slug':str(self.slug)})
    def __unicode__(self):
        return self.name

