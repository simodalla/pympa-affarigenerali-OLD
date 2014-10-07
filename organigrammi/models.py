# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone

from model_utils.models import TimeStampedModel


class RangeValiditaModel(models.Model):
    inizio_validita = models.DateTimeField(verbose_name='Data inizio validita',
                                           default=timezone.now)
    fine_validita = models.DateTimeField(verbose_name='Data fine validita',
                                         blank=True, null=True)

    class Meta:
        abstract = True


@python_2_unicode_compatible
class Ente(TimeStampedModel, RangeValiditaModel):
    nome = models.CharField(max_length=200, unique=True)
    ente_padre = models.ForeignKey('self', blank=True, null=True)

    class Meta:
        verbose_name = 'Ente'
        verbose_name_plural = 'Enti'

    def __str__(self):
        return '{} {}'.format(self.nome)


@python_2_unicode_compatible
class Persona(TimeStampedModel, RangeValiditaModel):
    cognome = models.CharField(max_length=80, verbose_name='Cognome')
    nome = models.CharField(max_length=80, verbose_name='Nome')
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                verbose_name='Utente del sistema',
                                blank=True, null=True)
    ente = models.ForeignKey(Ente, blank=True, null=True)

    class Meta:
        verbose_name = 'Persona'
        verbose_name_plural = 'Persone'

    def __str__(self):
        return '{} {}'.format(self.cognome, self.nome)


@python_2_unicode_compatible
class Mandato(TimeStampedModel, RangeValiditaModel):
    ente = models.ForeignKey(Ente)
    boss = models.OneToOneField(
        Persona, verbose_name="Sindaco o Presidente dell'unione",
        related_name='boss_mandato', blank=True, null=True)
    vice = models.OneToOneField(
        Persona, verbose_name="Vicesindaco o Vicepresidente  dell'unione",
        related_name='vice_mandato', blank=True, null=True)
    speacker = models.OneToOneField(
        Persona, verbose_name='Presidente del consiglio',
        related_name='speacker_mandato', blank=True, null=True)

    class Meta:
        verbose_name = 'Mandato'
        verbose_name_plural = 'Mandati'

    def __str__(self):
        return '{} dal {} al {}'.format(
            self.ente.nome, self.data_inizio, self.data_fine)


@python_2_unicode_compatible
class GruppoConsigliare(TimeStampedModel, RangeValiditaModel):
    mandato = models.ForeignKey(Mandato)
    nome = models.CharField(max_length=200)

    def __str__(self):
        return '[{}] {}'.format(self.ente.nome, self.nome)

    class Meta:
        verbose_name = 'Gruppo Consigliare'
        verbose_name_plural = 'Gruppo Consigliari'


@python_2_unicode_compatible
class Assessore(TimeStampedModel, RangeValiditaModel):
    mandato = models.ForeignKey(Mandato)
    persona = models.OneToOneField(Persona)
    delega = models.CharField(max_length=500)

    class Meta:
        verbose_name = 'Assessore'
        verbose_name_plural = 'Assessori'

    def __str__(self):
        return '{}, {}'.format(self.persona, self.delega)


@python_2_unicode_compatible
class Consigliere(TimeStampedModel, RangeValiditaModel):
    mandato = models.ForeignKey(Mandato)
    persona = models.ForeignKey(Persona)
    gruppoconsigliare = models.ForeignKey(GruppoConsigliare,
                                          blank=True, null=True)

    class Meta:
        verbose_name = 'Consigliere'
        verbose_name_plural = 'Consiglieri'

    def __str__(self):
        return 'Consigliere {}'.format(self.persona)


class SessioneAssembla(TimeStampedModel):
    data = models.DateField(default=timezone.datetime.date)


class SessioneGiunta(SessioneAssembla):
    assessori = models.ManyToManyField(Assessore, blank=True, null=True)


class SessioneConsiglioComunale(SessioneAssembla):
    consiglieri = models.ManyToManyField(Assessore, blank=True, null=True)
