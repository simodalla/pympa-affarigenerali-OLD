#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from unittest import mock

import pytest

from django.contrib import admin
from django.utils import timezone


from organigrammi.admin import SessioneAssembleaAdmin
from organigrammi.models import SessioneAssemblea, Mandato, Ente, Consiglio


@pytest.fixture
def sessione_admin():
    return SessioneAssembleaAdmin(SessioneAssemblea, admin.AdminSite)


@pytest.fixture
def sessione_without_presenze():
    mandato = Mandato.objects.create(ente=Ente.objects.create(titolo='ente'))
    assemblea = Consiglio.objects.create(mandato=mandato)
    return SessioneAssemblea.objects.create(
        data_svolgimento=timezone.now(), content_object=assemblea)


@pytest.mark.django_db
class TestSessioneAssembleaAdmin(object):

    @mock.patch.object(SessioneAssemblea, 'create_presenze')
    @mock.patch('django.contrib.admin.ModelAdmin.change_view')
    def test_change_view_call_create_presenze(
            self, mock_change_view, mock_create_presenze,
            rf, sessione_admin, sessione_without_presenze):
        # s = SessioneAssembleaAdmin(SessioneAssemblea, admin.AdminSite)
        print(sessione_without_presenze)
        print(sessione_without_presenze.presenze.all())
        sessione_admin.change_view(rf.get('/fake/'),
                                   sessione_without_presenze.pk)
        mock_create_presenze.assert_called_once_with()




