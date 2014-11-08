# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import datetime

from django.views.generic.edit import FormView

from .models import Presenza, SessioneAssemblea, Mandato
from .forms import FilterRiepiloghiPresenze


class RiepiloghiPresenzeFormView(FormView):
    template_name = "organigrammi/presenze_visualizzazione.html"
    form_class = FilterRiepiloghiPresenze

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
                SessioneAssemblea.objects.related_content_types_ids()),
            'assessori': (
                False if not self.request.GET.get('assessori', None) else True)
        }
        return results

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
        sessioni = SessioneAssemblea.objects.filter_for_riepilogo(
            mandato, request_data['from_date'], request_data['to_date'],
            content_type_ids=request_data['tipi_assemblea'])
        context['table_header'] = (
            [''] +
            ['{}'.format(sessione) for sessione in sessioni] +
            ['Totale Presenze',
             'Totale Gettoni',
             'Costo Totale Gettoni (&#8364;)'])
        context['table_rows'] = Presenza.objects.get_matrix_for_riepilogo(
            mandato, sessioni, with_assessori=request_data['assessori'])
        return context