# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import datetime

from django.views.generic.base import TemplateView
from .models import Presenza, SessioneAssemblea


class RiepiloghiPresenzeView(TemplateView):

    template_name = "organigrammi/presenze_visualizzazione.html"

    def _get_date_from_kwargs(self, kwargs, prefix):
        return datetime.date(year=int(kwargs[prefix + '_year']),
                             month=int(kwargs[prefix + '_month']),
                             day=int(kwargs[prefix + '_day']))

    def get_context_data(self, **kwargs):
        from_date = self._get_date_from_kwargs(kwargs, 'from')
        to_date = self._get_date_from_kwargs(kwargs, 'to')
        context = super(RiepiloghiPresenzeView, self).get_context_data(
            **kwargs)
        context['title'] = 'Riepiloghi Presenze'
        # context['presenze'] = Presenza.objects.all()
        sessioni = SessioneAssemblea.objects.filter(
            data_svolgimento__range=(from_date, to_date))
        context['sessioni'] = sessioni
        return context