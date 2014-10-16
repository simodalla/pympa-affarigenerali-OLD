#!/usr/bin/env python
# -*- coding: utf-8 -*-


from unittest import mock

from django.test import TestCase
from django.utils import timezone

from organigrammi.models import (SessioneAssemblea, Presenza, Consiglio,
                                 Mandato, Ente, Persona)


class TestSessioneAssemblea(TestCase):

    def make_componenti(self, n=2):
        return [Persona.objects.create(cognome='cp%s' % i, nome='np%s' % i)
                for i in range(0, n)]

    def setUp(self):
        self.mandato = Mandato.objects.create(
            ente=Ente.objects.create(titolo='ente'))
        self.assemblea = Consiglio.objects.create(mandato=self.mandato)
        self.sessione = SessioneAssemblea.objects.create(
            data_svolgimento=timezone.now(), content_object=self.assemblea)

    @mock.patch('organigrammi.models.Assemblea.componenti',
                new_callable=mock.PropertyMock)
    def test_create_presenze(self, mock_componenti):
        mock_componenti.return_value = self.make_componenti(2)
        presenze = self.sessione.create_presenze()
        self.assertEqual(len(presenze), len(self.assemblea.componenti))
        for field, expected in [('sessione', {self.sessione}),
                                ('persona', set(self.assemblea.componenti)),
                                ('presenza', {False})]:
            self.assertSetEqual({getattr(p, field) for p, create in presenze},
                                expected,
                                msg='error into "Presenza" field "%s"' % field)
