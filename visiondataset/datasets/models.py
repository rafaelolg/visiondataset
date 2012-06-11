import uuid
import os
import string
import logging

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
from StringIO import StringIO
from zipfile import ZipFile

from util import base_name

DEFAULT_DTYPE_TEMPLATE='''<a href="${file_url}">${file_name}</a> '''
DEFAULT_DTYPE_CREATE_THUMBNAIL='''convert -resize 160x $file_name $thumbnail_file_name'''
LOGGER = logging.getLogger(__name__)



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

    def to_zip(self):
        """Creates a zip file (StringIO) with the datums of this dataset"""
        inmemory = StringIO()
        zipf = ZipFile(inmemory, 'w')
        for d in self.datum_set.filter():
            zipf.write(d.package.path, d.file_name())
        zipf.close()
        inmemory.seek(0)
        return inmemory

    def add_from_zip(self, zip_file, dtype, owner):
        """Add files of zip_file with dtype type to this Dataset"""
        from django.core.files.base import ContentFile
        zipf = ZipFile(zip_file, 'r')
        names = zipf.namelist()
        for name in names:
            if name.startswith('__') or name.startswith('.'): # do not process meta files
                continue
            LOGGER.debug('Processing %s' % name)
            data = zipf.read(name)
            d=Datum(dataset=self, owner=owner, name=name, dtype = dtype)
            d.package.save(name,ContentFile(data))
            d.save()
        zipf.close()




class DataType(models.Model):
    """docstring"""
    name = models.CharField(max_length=50)
    slug = AutoSlugField(_('slug'), populate_from='name')
    template_to_view = models.TextField(default=DEFAULT_DTYPE_TEMPLATE)
    create_thumbnail_command = models.TextField(default=DEFAULT_DTYPE_CREATE_THUMBNAIL)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('datatype_view',(),{'slug':str(self.slug)})

    def create_thumbnail(self, absolut_file_name, destination_dir):
        """"
        creates the thumbnail of absolut_file_name file into destination_dir
        Warning: be sure the create_thumbnail command is safe.
        """
        destination_dir = os.path.join(settings.SENDFILE_ROOT, destination_dir)
        try:
            os.mkdir(destination_dir)
        except:
            pass
        basename = base_name(absolut_file_name) + '.png'
        thumbnail_file_name = os.path.join(destination_dir,basename)
        if not os.path.exists(thumbnail_file_name):
            template = string.Template(self.create_thumbnail_command.strip())
            cmd = template.safe_substitute(file_name=absolut_file_name,
                    thumbnail_file_name=thumbnail_file_name)
            LOGGER.debug('creating thumbnail:'+cmd)

            os.system(cmd)
        return thumbnail_file_name

protected_storage = FileSystemStorage(location=settings.SENDFILE_ROOT)
def get_package_file_path(instance, filename, prefix='datum'):
    #TODO: isso tem que ser mais robusto
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

    def thumbnail_url(self):
        url= reverse('datasets_datum_thumbnail', kwargs={'dataset_id':self.dataset_id, 'pk':self.pk})
        return url

    def file_name(self):
        #TODO:isso tem que ser mais robusto
        return slugify(self.name) + '.' + self.package.name.split('.')[-1]

    def file_render(self):
        template = string.Template(self.dtype.template_to_view)
        text = template.safe_substitute(file_url=self.file_url(), file_name=self.file_name())
        return text

    def get_thumbnail_file_path(self):
        return self.dtype.create_thumbnail(self.package.path,'datum_thumbnails')
