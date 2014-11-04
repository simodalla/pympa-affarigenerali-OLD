# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import (GenericForeignKey,
                                                GenericRelation)
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
        ordering = ('cognome', 'nome')
        verbose_name = 'Persona'
        verbose_name_plural = 'Persone'

    def __str__(self):
        return '{} {}'.format(self.cognome, self.nome)

    def get_absolute_url(self):
        return '{}?id={}'.format(
            reverse(admin_urlname(self._meta, 'changelist')), self.pk,)


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
    mandato = models.ForeignKey(Mandato, related_name='assessori')
    persona = models.OneToOneField(Persona)
    delega = models.CharField(max_length=500)

    class Meta:
        verbose_name = 'Assessore'
        verbose_name_plural = 'Assessori'

    def __str__(self):
        return 'Ass. {}'.format(self.persona)

    def get_absolute_url(self):
        return '{}?id={}'.format(
            reverse(admin_urlname(self._meta, 'changelist')), self.pk,)


@python_2_unicode_compatible
class Consigliere(TimeStampedModel, RangeValiditaModel):
    mandato = models.ForeignKey(Mandato, related_name='consiglieri')
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


class SessioneAssemblea(TimeStampedModel):
    data_svolgimento = models.DateField()
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ('data_svolgimento',)
        verbose_name = 'Sessione Assemblea'
        verbose_name_plural = 'Sessioni Assemblea'
        unique_together = ('data_svolgimento', 'object_id', 'content_type', )

    def __str__(self):
        return '{} del {:%d/%m/%Y}'.format(str(self.content_type.name),
                                           self.data_svolgimento)

    @property
    def assemblea(self):
        return self.content_type.get_object_for_this_type(pk=self.object_id)

    def create_presenze_of_componenti(self):
        """
        :return: list of tuples (Presenza object, created) for all
                 assemblea.componenti
        :rtype: list[(organigrammi.models.Presenza, boolean),]
        """
        assemblea = self.content_type.get_object_for_this_type(
            pk=self.object_id)
        return [Presenza.objects.get_or_create(sessione=self,
                                               persona=componente)
                for componente in assemblea.componenti]


class Assemblea(TimeStampedModel):
    sessioni = GenericRelation(SessioneAssemblea)

    class Meta:
        abstract = True

    @property
    def ld_componenti(self):
        raise NotImplemented()

    @property
    def componenti(self):
        return Persona.objects.filter(pk__in=self.pks_componenti)

    @property
    def pks_componenti(self):
        """
        :return: iterable of ids of Persone objects that are componenti
        :rtype: iterable
        """
        raise NotImplemented()

    def has_componente(self, persona):
        """
        Return if Persona object passed into args is in defaul componenti
        propperty

        :param persona:
        :type persona: organigrammi.models.Persona
        :rtype: bool
        """
        return True if persona.pk in self.pks_componenti else False


class Consiglio(Assemblea):
    mandato = models.OneToOneField(Mandato)

    class Meta:
        verbose_name = 'Consiglio'
        verbose_name_plural = 'Consigli'

    @property
    def ld_componenti(self):
        return (
            [(c.get_absolute_url(), '{} ({})'.format(c, ruolo))
             for c, ruolo in [(self.mandato.boss, 'Sindaco'),
                              (self.mandato.speacker, 'Presidente')]]
            + [(c.get_absolute_url(), '{} (Assessore)'.format(c.persona))
               for c in self.mandato.assessori.all()]
            + [(c.get_absolute_url(), '{} (Consigliere)'.format(c.persona))
               for c in self.mandato.consiglieri.all()]
        )


class Giunta(Assemblea):
    mandato = models.OneToOneField(Mandato)

    class Meta:
        verbose_name = 'Giunta'
        verbose_name_plural = 'Giunte'

    @property
    def ld_componenti(self):
        return (
            [(self.mandato.boss.get_absolute_url(), '{} ({})'.format(
                self.mandato.boss, 'Sindaco'))]
            + [(c.get_absolute_url(), '{} (Assessore)'.format(c.persona))
               for c in self.mandato.assessori.all()]
        )


class CommissioneConsigliare(Assemblea):
    mandato = models.ForeignKey(Mandato)
    titolo = models.CharField(max_length=500)
    boss = models.OneToOneField(
        Consigliere, verbose_name="Presidente della commissione",
        related_name='boss_commissione', blank=True, null=True)
    vice = models.OneToOneField(
        Consigliere, verbose_name="Vicepresidente della commissione",
        related_name='vice_commisione', blank=True, null=True)
    consiglieri = models.ManyToManyField(Consigliere, blank=True, null=True)

    class Meta:
        verbose_name = 'Commissione Consigliare'
        verbose_name_plural = 'Commissioni Consigliari'

    @property
    def ld_componenti(self):
        result = ([(c.get_absolute_url(), '{} ({})'.format(c.persona, ruolo))
                   for c, ruolo in [(self.boss, 'Presidente'),
                                    (self.vice, 'Vice')]] +
                  [(c.get_absolute_url(), c.persona)
                   for c in self.consiglieri.all()])
        return result

    @property
    def pks_componenti(self):
        ids = set([self.boss.persona.pk, self.vice.persona.pk] +
                  list(self.consiglieri.values_list('persona_id', flat=True)))
        return ids


class Presenza(TimeStampedModel):
    persona = models.ForeignKey(Persona)
    sessione = models.ForeignKey(SessioneAssemblea, related_name='presenze')
    presenza = models.BooleanField(default=False, blank=True)

    class Meta:
        verbose_name = 'Presenza'
        verbose_name_plural = 'Presenze'
        unique_together = ('sessione', 'persona')

    def is_of_componente(self):
        if self.sessione.assemblea.has_componente(self.persona):
            return True
        return False
