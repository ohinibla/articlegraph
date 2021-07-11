# -*- coding: utf-8 -*-
from django import forms
from models import Site

class CreateForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = ['url']