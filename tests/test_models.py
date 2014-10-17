#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest

from unittest import mock

from django.test import TestCase
from django.utils import timezone

from organigrammi.models import (SessioneAssemblea, Consiglio,
                                 Mandato, Ente, Persona,)


class TestSessioneAssembleaModel(TestCase):

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
        presenze = self.sessione.create_presenze_of_componenti()
        self.assertEqual(len(presenze), len(self.assemblea.componenti))
        for field, expected in [('sessione', {self.sessione}),
                                ('persona', set(self.assemblea.componenti)),
                                ('presenza', {False})]:
            self.assertSetEqual({getattr(p, field) for p, create in presenze},
                                expected,
                                msg='error into "Presenza" field "%s"' % field)


@pytest.fixture
def assemblea_generica():
    from organigrammi.models import Assemblea
    assemblea = Assemblea()
    type(assemblea).pks_componenti = mock.PropertyMock(return_value=[1, 2, 3])
    return assemblea


@pytest.fixture
def presenza(assemblea_generica):
    from organigrammi.models import Presenza, SessioneAssemblea

    obj = Presenza()
    obj.persona = mock.MagicMock(spec_set=Persona)
    obj.sessione = mock.MagicMock(spec_set=SessioneAssemblea,
                                       assemblea=assemblea_generica)
    return obj


class TestAssembleaModel(object):

    def test_has_componente_return_true(self, assemblea_generica):
        persona = mock.MagicMock(spec_set=Persona)
        persona.pk = assemblea_generica.pks_componenti[0]
        assert assemblea_generica.has_componente(persona) is True

    def test_has_componente_return_false(self, assemblea_generica):
        persona = mock.MagicMock(spec_set=Persona, pk=1000)
        assert assemblea_generica.has_componente(persona) is False


class TestPresenzaModel(object):
    def test_is_of_componente_return_true(self, presenza):
        print(presenza)
        # assert p.is_of_componente() is True