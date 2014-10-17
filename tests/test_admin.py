#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from unittest import mock

import pytest

from django.contrib import admin
from django.utils import timezone


from organigrammi.admin import SessioneAssembleaAdmin
from organigrammi.models import (SessioneAssemblea, Mandato, Ente, Consiglio,
                                 Presenza)

from .factories import PersonaF

@pytest.fixture
def sessione_admin():
    """
    Return SessioneAssembleaAdmin class
    """
    return SessioneAssembleaAdmin(SessioneAssemblea, admin.AdminSite)


@pytest.fixture
def sessione_without_presenze():
    """
    Return an SessioneAssemblea object for an Assmblea of 'type' Consiglio
    """
    mandato = Mandato.objects.create(ente=Ente.objects.create(titolo='ente'))
    assemblea = Consiglio.objects.create(mandato=mandato)
    return SessioneAssemblea.objects.create(
        data_svolgimento=timezone.now(), content_object=assemblea)


@pytest.mark.django_db
class TestSessioneAssembleaAdmin(object):

    @mock.patch.object(SessioneAssemblea, 'create_presenze')
    @mock.patch('django.contrib.admin.ModelAdmin.change_view')
    def test_test_create_presenze_is_called_into_change_view(
            self, mock_change_view, mock_create_presenze,
            rf, sessione_admin, sessione_without_presenze):
        """
        Test that in change_view method called on SessioneAssemble object
        without related Presenze objects, method 'create_presenze' is called.
        """
        sessione_admin.change_view(rf.get('/fake/'),
                                   sessione_without_presenze.pk)
        mock_create_presenze.assert_called_once_with()

    @mock.patch.object(SessioneAssemblea, 'create_presenze')
    @mock.patch('django.contrib.admin.ModelAdmin.change_view')
    def test_create_presenze_is_not_call_into_change_view(
            self, mock_change_view, mock_create_presenze,
            rf, sessione_admin, sessione_without_presenze):
        Presenza.objects.create(persona=PersonaF(),
                                sessione=sessione_without_presenze,
                                presenza=False)
        sessione_admin.change_view(rf.get('/fake/'),
                                   sessione_without_presenze.pk)
        assert mock_create_presenze.called is False

    # def test_f(self):
    #     from .factories import MandatoGothamCity
    #     m = MandatoGothamCity()
    #     print(m, m.ente)
    #     # print(gc)
    #     # print(gc.inizio_validita)
    #     # print(gc.fine_validita)




