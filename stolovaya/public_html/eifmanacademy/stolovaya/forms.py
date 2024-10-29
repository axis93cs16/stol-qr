# coding: utf-8
from django import forms

class NumberForm(forms.Form):
    zavtrak = forms.BooleanField(label="zavtrak")
    obed = forms.BooleanField(label="obed")