# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.db.models import Manager, Q
from django.utils.timezone import now

from .exceptions import NotAPerson


class RangeValiditaManager(Manager):

    # def validi_tra(self, inizio_validita, fine_validita=None):

    def validi(self):
        return self.filter(
            Q(inizio_validita__lte=now()),
            Q(fine_validita__gte=now()) | Q(fine_validita__isnull=True),)


class SessioneAssembleaManager(Manager):

    def related_content_types(self):
        return set(self.order_by('content_type__name').values_list(
            'content_type__pk', 'content_type__name'))

    def related_content_types_ids(self):
        return [ct[0] for ct in self.related_content_types()]

    def filter_for_riepilogo(self, mandato, from_date, to_date,
                             content_type_ids=None):
        result = self.model.objects.filter(
            data_svolgimento__range=(from_date, to_date))
        if content_type_ids:
            result = result.filter(content_type__pk__in=content_type_ids)
        return [sessione for sessione in result.order_by('data_svolgimento')
                if sessione.content_object.mandato.pk == mandato.pk]


class PersonaManager(RangeValiditaManager):

    def get_persona_obj(self, obj):
        result = (obj if isinstance(obj, self.model)
                  else getattr(obj, 'persona', None))
        if not result:
            raise NotAPerson()
        return result


PRESENZA_SIMBOLI = {
    'presenza': 'P',
    'assenza': 'A',
    'non_previsto': '-',
    'not_a_number': 'NaP'}


class PresenzaManager(Manager):

    def get_data_for_riepilogo(self, componente, sessione):
        from .models import Persona
        try:
            persona = Persona.objects.get_persona_obj(componente)
            presenza = self.model.objects.get(
                persona=persona, sessione=sessione)
            data = (PRESENZA_SIMBOLI['presenza']
                    if presenza.presenza is True
                    else PRESENZA_SIMBOLI['assenza'],
                    sessione.get_costo_presenza(persona))
        except self.model.DoesNotExist:
            data = (PRESENZA_SIMBOLI['non_previsto'], 0)
        except NotAPerson:
            data = (PRESENZA_SIMBOLI['not_a_number'], 0)
        return data

    def get_matrix_for_riepilogo(self, mandato, sessioni, with_assessori=True):
        matrix = [
            [(componente, componente._meta.model_name)] +
            [self.model.objects.get_data_for_riepilogo(componente, sessione)
             for sessione in sessioni]
            for componente in mandato.get_componenti(
                with_assessori=with_assessori)]
        for ix, row in enumerate(matrix):
            presenze = list(filter(
                lambda x: x[0] == PRESENZA_SIMBOLI['presenza'], row[1:]))
            gettoni = list(filter(
                lambda x: x[0] == PRESENZA_SIMBOLI['presenza'] and x[1] > 0,
                row[1:]))
            matrix[ix] += [len(presenze),
                           len(gettoni),
                           sum([c for s, c in presenze])]
        matrix.append([sum(x) for x in list(zip(*matrix))[-3:]])
        return matrix

