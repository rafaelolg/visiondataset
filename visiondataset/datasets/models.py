import uuid
import os

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django_extensions.db.fields import CreationDateTimeField, AutoSlugField
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from guardian.shortcuts import get_users_with_perms
from visiondataset.base.models import UserProfile

DEFAULT_DTYPE_TEMPLATE='''<a href="%(file_url)s">%(file_name)s</a>'''

class Dataset(models.Model):
    """Set of datums"""
    name = models.CharField(max_length=256)
    owner = models.ForeignKey(User, related_name='+')
    created = CreationDateTimeField(_('created'))

    class Meta:
        permissions = (
            ('dataset_colaborate',
                _('View Edit Information and Colaborate with Dataset')),
        )
        get_latest_by = 'created'
        ordering = ('-created',)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('datasets_dataset_detail',(),{'pk':self.pk})

    def colaborators(self):
        users = get_users_with_perms(self)
        profiles = UserProfile.objects.filter(user__in=users)
        return profiles

class DataType(models.Model):
    """docstring"""
    name = models.CharField(max_length=50)
    slug = AutoSlugField(_('slug'), populate_from='name')
    template_to_view = models.TextField(default=DEFAULT_DTYPE_TEMPLATE)
    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('datatype_view',(),{'slug':str(self.slug)})



protected_storage = FileSystemStorage(location=settings.SENDFILE_ROOT)
def get_package_file_path(instance, filename, prefix='datum'):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join(prefix,filename)

class Datum(models.Model):
    """Data element"""
    dataset = models.ForeignKey(Dataset)
    owner = models.ForeignKey(User, related_name='+')
    created = CreationDateTimeField(_('created'))
    name = models.CharField(max_length=256)
    package = models.FileField(_("file"), upload_to=get_package_file_path, max_length=100,
            storage=protected_storage)
    dtype = models.ForeignKey(DataType,verbose_name= _("Type"), related_name='+',
            blank=False, default=1)

    class Meta:
        get_latest_by = 'created'
        ordering = ('dataset','-created')

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('datasets_datum_detail',(),{'dataset_id':self.dataset_id, 'pk':self.pk})

    def is_user_allowed(self, user):
        allowed = self.owner == user
        if not allowed:
            allowed = user.has_perm('dataset_colaborate', self)
        return allowed

    def file_url(self):
        return reverse('datasets_datum_file', kwargs={'dataset_id':self.dataset_id, 'pk':self.pk})

    def file_name(self):
        return slugify(self.name) + '.' + self.package.name.split('.')[-1]

    def file_render(self):
        text = self.dtype.template_to_view % {'file_url':self.file_url(), 'file_name':
                    self.file_name()}
        return text
