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
            result.filter(content_type__pk__in=content_type_ids)
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
    'presenza': 'X',
    'assenza': 'A',
    'non_previsto': 'A',
    'not_a_number': 'NaP'}


class PresenzaManager(Manager):

    def get_simbolo(self, persona, sessione):
        from .models import Persona
        try:
            presenza = self.model.objects.get(
                persona=Persona.objects.get_persona_obj(persona),
                sessione=sessione)
            simbolo = (PRESENZA_SIMBOLI['presenza']
                       if presenza.presenza is True
                       else PRESENZA_SIMBOLI['assenza'])
        except self.model.DoesNotExist:
            simbolo = PRESENZA_SIMBOLI['non_previsto']
        except NotAPerson:
            simbolo = PRESENZA_SIMBOLI['not_a_number']
        return simbolo

    def get_matrix_for_riepilogo(self, mandato, sessioni):
        matrix = [
            [componente] + [(self.model.objects.get_simbolo(componente,
                                                            sessione),
                             sessione.content_object.costo_presenza)
                            for sessione in sessioni]
            for componente in mandato.get_componenti()]
        a = lambda x: x[0]
        print("---->", a(tuple([1, 2])))
        for ix, row in enumerate(matrix):
            f_row = list(filter(
                lambda x: x[0] == PRESENZA_SIMBOLI['presenza'], row[1:]))
            matrix[ix].append((len(f_row), sum([c for s, c in f_row])))
            # print)
            # print([c for s, c in filter(lambda x: x[0] == PRESENZA_SIMBOLI['presenza'], row[1:])])

            # print(sum([c for s, c in list(]))
            # print(list(filter(lambda x: x[0] == PRESENZA_SIMBOLI['presenza'], row)))
            # costo_presenze
            # n_presenze = [for row[1:]]
            # print(ix, row)
            # print(row[1:], row[1:].count(PRESENZA_SIMBOLI['presenza']))
        print(matrix)
        return matrix

