# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import datetime

from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from .models import Presenza, SessioneAssemblea, Mandato


# ####################################################
from django import forms


class RangeDateForm(forms.Form):
    # your_name = forms.CharField(label='Your name', max_length=100)
    from_date = forms.DateField(label='Dalla data:', required=False)
    to_date = forms.DateField(label='alla data:', required=False)
    tipi_assemblea = forms.ChoiceField(label='tipi assembla', required=False,
                                       widget=forms.CheckboxSelectMultiple)

    def __init__(self, *args, **kwargs):
        super(RangeDateForm, self).__init__(*args, **kwargs)
        for field in ['from_date', 'to_date']:
            # self.fields[field].required = True
            self.fields[field].widget.attrs['class'] = 'range_date_field'
        self.fields['tipi_assemblea'].choices = (
            SessioneAssemblea.objects.related_content_types())


class RiepiloghiPresenzeFormView(FormView):
    template_name = "organigrammi/presenze_visualizzazione.html"
    form_class = RangeDateForm

    def get_request_data(self):
        today = datetime.date.today()
        first_of_year = datetime.date(year=today.year, month=1, day=1)
        date_format = '%d/%m/%Y'
        results = {
            'from_date': datetime.datetime.strptime(
                self.request.GET.get(
                    'from_date', first_of_year.strftime(date_format)),
                date_format),
            'to_date': datetime.datetime.strptime(
                self.request.GET.get(
                    'to_date', today.strftime(date_format)),
                date_format),
            'tipi_assemblea': (
                self.request.GET.getlist('tipi_assemblea') or
                SessioneAssemblea.objects.related_content_types_ids())}
        return results

    def get_simbolo(self, persona, sessione):
        try:
            presenza = Presenza.objects.get(persona=persona,
                                            sessione=sessione)
            simbolo = 'X' if presenza.presenza is True else 'A'
        except Presenza.DoesNotExist:
            simbolo = '-'
        return simbolo

    def get_initial(self):
        initial = super(RiepiloghiPresenzeFormView, self).get_initial() or {}
        initial.update(self.get_request_data())
        return initial

    def get_context_data(self, *args, **kwargs):

        context = super(RiepiloghiPresenzeFormView, self).get_context_data(
            **kwargs)
        context['title'] = 'Riepiloghi Presenze'
        try:
            mandato = Mandato.objects.get(pk=self.kwargs['mandato_pk'])
            context['mandato'] = mandato
        except Mandato.DoesNotExist:
            context['mandato_does_not_exist'] = True
            return context
        request_data = self.get_request_data()
        sessioni = [
            sessione for sessione in SessioneAssemblea.objects.filter(
                data_svolgimento__range=(request_data['from_date'],
                                         request_data['to_date']),
                content_type__pk__in=request_data['tipi_assemblea']).order_by(
                    'data_svolgimento')
            if sessione.content_object.mandato.pk == mandato.pk]
        # print("ass: ", ass)
        # # import ipdb
        # # ipdb.set_trace()
        # assemblee = [mandato.consiglio, mandato.giunta] + list(
        #     mandato.commissioniconsigliari.all())
        # sessioni_pks = [sessione for assemblea
        #                 in assemblee for sessione
        #                 in assemblea.sessioni.values_list('pk', flat=True)]
        # sessioni = SessioneAssemblea.objects.filter(
        #     data_svolgimento__range=(request_data['from_date'],
        #                              request_data['to_date']),
        #     pk__in=sessioni_pks).order_by('data_svolgimento')

        context['table_header'] = [''] + ['{}'.format(sessione)
                                          for sessione in sessioni]
        context['table_rows'] = [
            [componente] + [self.get_simbolo(componente, sessione)
                            for sessione in sessioni]
            for componente in mandato.get_componenti()]
        return context