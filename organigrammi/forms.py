# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django import forms

from .models import SessioneAssemblea


class FilterRiepiloghiPresenze(forms.Form):
    from_date = forms.DateField(label='Dalla data:', required=False)
    to_date = forms.DateField(label='Alla data:', required=False)
    tipi_assemblea = forms.ChoiceField(label='Tipi assembla', required=False,
                                       widget=forms.CheckboxSelectMultiple)
    assessori = forms.BooleanField(label='Mostra assessori', required=False,
                                   initial=True)

    def __init__(self, *args, **kwargs):
        super(FilterRiepiloghiPresenze, self).__init__(*args, **kwargs)
        for field in ['from_date', 'to_date']:
            self.fields[field].widget.attrs['class'] = 'range_date_field'
        self.fields['tipi_assemblea'].choices = (
            SessioneAssemblea.objects.related_content_types())
