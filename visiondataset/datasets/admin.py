#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from models import Dataset, Datum

class DatasetAdmin(admin.ModelAdmin):
    pass

class DatumAdmin(admin.ModelAdmin):
    pass


admin.site.register(Datum, DatumAdmin)
admin.site.register(Dataset, DatasetAdmin)


# admin.py
