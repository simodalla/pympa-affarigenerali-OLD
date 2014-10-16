#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_openpa-organigrammi
------------

Tests for `openpa-organigrammi` models module.
"""

from django.test import TestCase
from django.utils import timezone
from unittest import mock

from organigrammi.models import (SessioneAssemblea, Presenza, Consiglio,
                                 Mandato, Ente, Persona)


def make_componenti(n=2):
    return [Persona.objects.create(cognome='cp%s' % i, nome='np%s' % i)
            for i in range(0, n)]


class TestSessioneAssemblea(TestCase):

    def setUp(self):
        self.mandato = Mandato.objects.create(
            ente=Ente.objects.create(titolo='ente'))
        self.assemblea = Consiglio.objects.create(mandato=self.mandato)
        self.sessione = SessioneAssemblea.objects.create(
            data_svolgimento=timezone.now(), content_object=self.assemblea)

    @mock.patch('organigrammi.models.Assemblea.componenti',
                new_callable=mock.PropertyMock(
                    return_value=make_componenti(2)))
    def test_create_presenze(self, mock_componenti):
        presenze = self.sessione.create_presenze()
        self.assertEqual(len(presenze), len(self.assemblea.componenti))
        for field, expected in [('sessione', {self.sessione}),
                                ('persona', set(self.assemblea.componenti)),
                                ('presenza', {False})]:
            self.assertSetEqual({getattr(p, field) for p, create in presenze},
                                expected,
                                msg='error into "Presenza" field "%s"' % field)
