from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField, AutoSlugField


class Dataset(models.Model):
    """Set of datums"""
    name = models.CharField(max_length=256)
    slug = AutoSlugField(_('slug'), populate_from='name')
    owner = models.ForeignKey(User, related_name='+')
    created = CreationDateTimeField(_('created'))

    class Meta:
        permissions = (
            ('view_dataset', _('View Dataset')),
            ('add_datum_dataset', _('Add elements')),
        )
        get_latest_by = 'created'
        ordering = ('-created',)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('dataset.views.datatype',(),{'slug':str(self.slug)})


class DataType(models.Model):
    """docstring"""
    name = models.CharField(max_length=50)
    slug = AutoSlugField(_('slug'), populate_from='name')

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('dataset.views.datatype',(),{'slug':str(self.slug)})


class Datum(models.Model):
    """Data element"""
    dataset = models.ForeignKey(Dataset, related_name='+')
    owner = models.ForeignKey(User, related_name='+')
    created = CreationDateTimeField(_('created'))
    name = models.CharField(max_length=256)
    slug = AutoSlugField(_('slug'), populate_from='name')
    description = models.TextField(_('description'), blank=True)
    package = models.FileField(upload_to='datum', max_length=100)
    dtype = models.ForeignKey(DataType, related_name='+')

    class Meta:
        permissions = (
            ('view_datum', _('View Element Datum')),
        )
        get_latest_by = 'created'
        ordering = ('dataset','-created')

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('dataset.views.datatype',(),{'slug':str(self.slug)})

