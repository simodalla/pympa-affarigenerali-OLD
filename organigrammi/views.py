# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import datetime

from django.views.generic.base import TemplateView
from .models import Presenza, SessioneAssemblea, Mandato


class RiepiloghiPresenzeView(TemplateView):

    template_name = "organigrammi/presenze_visualizzazione.html"

    def _get_date_from_kwargs(self, kwargs, prefix):
        return datetime.date(year=int(kwargs[prefix + '_year']),
                             month=int(kwargs[prefix + '_month']),
                             day=int(kwargs[prefix + '_day']))

    # def get(self, request, *args, **kwargs):
    #
    #     return super(RiepiloghiPresenzeView, self).get(
    #         request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(RiepiloghiPresenzeView, self).get_context_data(
            **kwargs)
        context['title'] = 'Riepiloghi Presenze'
        try:
            mandato = Mandato.objects.get(pk=kwargs['mandato_pk'])
        except Mandato.DoesNotExist:
            context['mandato_does_not_exist'] = True
            return context
        today = datetime.date.today()
        range_date = {
            'from_date': datetime.date(year=today.year, month=1, day=1),
            'to_date': today}
        for key in range_date:
            get_param = self.request.GET.get(key, None)
            if get_param:
                range_date[key] = datetime.datetime.strptime(get_param,
                                                             '%d/%m/%Y')
        context.update(range_date)
        # context['presenze'] = Presenza.objects.all()

        assemblee = [mandato.consiglio, mandato.giunta] + list(
            mandato.commissioniconsigliari.all())
        sessioni_pks = [sessione for assemblea
                        in assemblee for sessione
                        in assemblea.sessioni.values_list('pk', flat=True)]
        from collections import OrderedDict
        sessioni = {s: {p.persona.pk: p for p
                        in s.presenze.order_by('persona__pk')} for s
                    in SessioneAssemblea.objects.filter(
                        data_svolgimento__range=(range_date['from_date'],
                                                 range_date['to_date']),
                        pk__in=sessioni_pks)}
        # sessioni = sorted(sessioni, key=lambda t: t.data_svolgimento)
        # print(sessioni)
        sessioni = OrderedDict(
            sorted(sessioni.items(), key=lambda t: t[0].data_svolgimento))
        context['sessioni'] = sessioni
        print(sessioni.keys())
        return context