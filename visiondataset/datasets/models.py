from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

class Dataset(models.Model):
    """Set of datums"""
    creation_time = models.TimeField(auto_now_add=True)
    owner = models.ForeignKey(User, null=False)
    class Meta:
        permissions = (
            ('view_dataset', _('View Dataset')),
            ('add_datum_dataset', _('Add elements')),
        )
        get_latest_by = 'creation_time'

class Datum(models.Model):
    """Data element"""
    dataset = models.ForeignKey(Dataset, null=False)
    owner = models.ForeignKey(User, null=False)
    creation_time = models.TimeField(auto_now_add=True)
    name = models.CharField(max_length=256, blank=False)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='datum', max_length=256)
    class Meta:
        permissions = (
            ('view_datum', _('View Element Datum')),
        )
        get_latest_by = 'creation_time'
