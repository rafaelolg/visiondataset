#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.forms import ModelForm
from models import Dataset, Datum


class DatasetModelForm(ModelForm):
    """Form for Dataset"""
    class Meta:
        model = Dataset
        exclude = ('owner', 'created')

class DatumModelForm(ModelForm):
    initial={'dtype': 1}
    class Meta:
        model = Datum
        exclude = ('name', 'owner', 'dataset', 'created')


# forms.py

