#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.forms import ModelForm
from models import Dataset, Datum
from django import forms
from django.forms import fields, models, formsets, widgets
from django.utils.translation import ugettext_lazy as _

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


class ColaboratorForm(forms.Form):
    user = forms.CharField(max_length=256, required=True, label=_('User or Email'))

    def __init__(self, *args, **kwargs):
        super(ColaboratorForm, self).__init__(*args, **kwargs)
        self.fields['user'].widget = widgets.TextInput(attrs={'class': 'autocomplete-me'})

    class Media:
        js = ('js/libs/jquery.autocomplete.min.js', 'js/libs/autocomplete-init.js',)
        css = {
            'all': ('css/jquery.autocomplete.css',),
        }

