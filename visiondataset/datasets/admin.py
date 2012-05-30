#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from models import Dataset, Datum, DataType

class DatasetAdmin(GuardedModelAdmin):
    pass

class DatumAdmin(GuardedModelAdmin):
    pass

class DataTypeAdmin(GuardedModelAdmin):
    pass

admin.site.register(Datum, DatumAdmin)
admin.site.register(Dataset, DatasetAdmin)
admin.site.register(DataType, DataTypeAdmin)


# admin.py
