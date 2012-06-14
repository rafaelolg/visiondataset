#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from models import Dataset, Datum, DataType, DatumAttachment

class DatasetAdmin(GuardedModelAdmin):
    list_display = ('name' , 'owner', 'created')
    search_fields = ['user__name']


class DataTypeAdmin(GuardedModelAdmin):
    pass

class DatumAttachmentAdmin(GuardedModelAdmin):
    list_display = ('name' , 'datum', 'owner', 'created')

class DatumAttachmentInlineAdmin(admin.TabularInline):
    model=DatumAttachment
    extra = 1


class DatumAdmin(GuardedModelAdmin):
    list_display = ('name' , 'dataset','owner', 'created')
    inlines = [ DatumAttachmentInlineAdmin, ]

admin.site.register(Datum, DatumAdmin)
admin.site.register(DatumAttachment, DatumAttachmentAdmin)
admin.site.register(Dataset, DatasetAdmin)
admin.site.register(DataType, DataTypeAdmin)


# admin.py
