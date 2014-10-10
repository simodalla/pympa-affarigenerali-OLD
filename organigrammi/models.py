# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.core.urlresolvers import reverse
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
    titolo = models.CharField(max_length=200, unique=True)
    ente_padre = models.ForeignKey('self', blank=True, null=True)

    class Meta:
        verbose_name = 'Ente'
        verbose_name_plural = 'Enti'

    def __str__(self):
        return '{}'.format(self.titolo)


@python_2_unicode_compatible
class Persona(TimeStampedModel, RangeValiditaModel):
    cognome = models.CharField(max_length=80, verbose_name='Cognome')
    nome = models.CharField(max_length=80, verbose_name='Nome')
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                verbose_name='Utente del sistema',
                                blank=True, null=True)
    ente = models.ForeignKey(Ente, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

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
    vice_speacker = models.OneToOneField(
        Persona, verbose_name='Vicepresidente del consiglio',
        related_name='vicespeacker_mandato', blank=True, null=True)

    class Meta:
        verbose_name = 'Mandato'
        verbose_name_plural = 'Mandati'

    def __str__(self):
        fine_validita = self.fine_validita or (self.inizio_validita +
                                               timezone.timedelta(
                                                   days=365 * 5))
        return 'Mandato {} {:%Y}-{:%Y}'.format(self.ente,
                                               self.inizio_validita,
                                               fine_validita)


@python_2_unicode_compatible
class GruppoConsigliare(TimeStampedModel, RangeValiditaModel):
    mandato = models.ForeignKey(Mandato)
    titolo = models.CharField(max_length=200)

    def __str__(self):
        return '[{}] {}'.format(self.mandato.ente, self.titolo)

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
        return 'Ass. {}'.format(self.persona)


@python_2_unicode_compatible
class Consigliere(TimeStampedModel, RangeValiditaModel):
    mandato = models.ForeignKey(Mandato)
    persona = models.ForeignKey(Persona)
    gruppoconsigliare = models.ForeignKey(GruppoConsigliare,
                                          blank=True, null=True)
    capogruppo = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Consigliere'
        verbose_name_plural = 'Consiglieri'

    def __str__(self):
        return 'Cons. {}'.format(self.persona)

    def get_absolute_url(self):
        return '{}?id={}'.format(
            reverse(admin_urlname(self._meta, 'changelist')), self.pk,)


class Assemblea(TimeStampedModel):
    mandato = models.ForeignKey(Mandato)


class Consiglio(Assemblea):

    class Meta:
        verbose_name = 'Consiglio'
        verbose_name_plural = 'Consigli'


class Giunta(Assemblea):
    class Meta:
        verbose_name = 'Giunta'
        verbose_name_plural = 'Giunte'


class CommissioneConsigliare(Assemblea):
    titolo = models.CharField(max_length=500)
    boss = models.OneToOneField(
        Consigliere, verbose_name="Presidente della commissione",
        related_name='boss_commissione', blank=True, null=True)
    vice = models.OneToOneField(
        Consigliere, verbose_name="Vicepresidente della commissione",
        related_name='vice_commisione', blank=True, null=True)
    componenti = models.ManyToManyField(Consigliere, blank=True, null=True)

    class Meta:
        verbose_name = 'Commissione Consigliare'
        verbose_name_plural = 'Commissioni Consigliari'


class SessioneAssembla(TimeStampedModel):
    data_svolgimento = models.DateField()
    assembla = models.ForeignKey(Assemblea)

    class Meta:
        verbose_name = 'Sessione Assembla'
        verbose_name_plural = 'Sessioni Assembla'
        unique_together = ('data_svolgimento', 'assembla')


class SessioneGiunta(SessioneAssembla):

    class Meta:
        verbose_name = 'Sessione di Giunta'
        verbose_name_plural = 'Sessioni di Giunta'


class SessioneConsiglio(SessioneAssembla):

    class Meta:
        verbose_name = 'Sessione di Consiglio'
        verbose_name_plural = 'Sessioni di Consiglio'


class SessioneCommissioneConsigliare(SessioneAssembla):

    class Meta:
        verbose_name = 'Sessione di Commissione Consigliare'
        verbose_name_plural = 'Sessioni di Commissione Consigliare'


class Presenza(TimeStampedModel):
    sessione = models.ForeignKey(SessioneAssembla)
    persona = models.ForeignKey(Persona)
    presenza = models.BooleanField(default=False, blank=True)

    class Meta:
        verbose_name = 'Presenza'
        verbose_name_plural = 'Presenze'
        unique_together = ('sessione', 'persona')