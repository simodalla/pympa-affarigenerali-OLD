# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import factory


class PersonaF(factory.django.DjangoModelFactory):
    class Meta:
        model = 'organigrammi.Persona'
        django_get_or_create = ('cognome',)

    cognome = factory.Sequence(lambda n: 'Doe %s' % n)
    nome = factory.Sequence(lambda n: 'John %s' % n)


class EnteF(factory.django.DjangoModelFactory):
    class Meta:
        model = 'organigrammi.Ente'
        django_get_or_create = ('titolo',)


class MandatoF(factory.django.DjangoModelFactory):
    class Meta:
        model = 'organigrammi.Mandato'


class SessioneAssembleaF(factory.django.DjangoModelFactory):
    class Meta:
        model = 'organigrammi.SessioneAssemblea'


class GothamCity(EnteF):
    titolo = 'Comune di Gotham City'


class MandatoGothamCity(MandatoF):
    ente = factory.SubFactory(GothamCity)


