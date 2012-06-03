#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.forms import ModelForm
from models import Dataset


class DatasetModelForm(ModelForm):
    """Form for Dataset"""
    class Meta:
        model = Dataset
        exclude = ('owner', 'created')

# forms.py

