# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib import admin

from .models import (Ente, Mandato, Persona, GruppoConsigliare, Assessore,
                     Consigliere, CommissioneConsigliare)


RANGE_VALIDITA_SECTION = ('Range di validità',
                          {'fields': ('inizio_validita', 'fine_validita')})


class GruppoConsigliareInline(admin.TabularInline):
    fields = ('titolo', 'inizio_validita', 'fine_validita')
    model = GruppoConsigliare
    extra = 1


class AssessoreInline(admin.TabularInline):
    fields = ('persona', 'delega', 'inizio_validita', 'fine_validita')
    model = Assessore
    extra = 1


class ConsigliereInline(admin.TabularInline):
    fields = ('persona', 'gruppoconsigliare', 'capogruppo')
    model = Consigliere
    extra = 1


@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('cognome', 'nome', 'email', 'ente', 'user')}),
        RANGE_VALIDITA_SECTION)
    list_display = ('cognome', 'nome', 'ente', 'user', 'inizio_validita',
                    'fine_validita')
    search_fields = ('cognome', 'nome', 'ente__titolo',)


@admin.register(Ente)
class EnteAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('titolo', 'ente_padre')}),
        RANGE_VALIDITA_SECTION)
    list_display = ('titolo', 'ente_padre')


@admin.register(Mandato)
class MandatoAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('ente', 'boss', 'vice', 'speacker',
                           'vice_speacker')}),
        RANGE_VALIDITA_SECTION)
    list_display = ('ente', 'inizio_validita', 'fine_validita', 'boss', 'vice',
                    'speacker')
    list_select_related = True
    inlines = [AssessoreInline, GruppoConsigliareInline, ConsigliereInline]


@admin.register(Consigliere)
class ConsigliereAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('persona', 'mandato', 'gruppoconsigliare',
                           'capogruppo',)}),
        RANGE_VALIDITA_SECTION)
    list_filter = ('gruppoconsigliare',)
    list_display = ('persona', 'mandato', 'gruppoconsigliare',
                    'capogruppo', 'inizio_validita', 'fine_validita')
    search_fields = ('persona__cognome', 'persona__nome',)


@admin.register(Assessore)
class AssessoreAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('persona', 'mandato', 'delega',)}),
        RANGE_VALIDITA_SECTION)
    list_filter = ('mandato',)
    list_display = ('persona', 'mandato', 'delega',
                    'inizio_validita', 'fine_validita')
    search_fields = ('persona__cognome', 'persona__nome', 'delega')


@admin.register(CommissioneConsigliare)
class CommissioneConsigliareAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('mandato', 'titolo', 'boss', 'vice',
                           'componenti')}),
    )
    filter_horizontal = ('componenti', )
    list_display = ('titolo', 'mandato', 'boss', 'vice', 'ld_componenti')
    list_filter = ('mandato',)
    search_fields = ('titolo', 'mandato__ente__titolo',)

    def ld_componenti(self, obj):
        """
        :type obj: organigrammi.models.CommissioneConsigliare
        """
        links = ['<a href="{}">{}</a>'.format(
            c.get_absolute_url(), c.persona) for c in obj.componenti.all()]
        return '<br />'.join(links)

    ld_componenti.short_description = 'Componenti'
    ld_componenti.allow_tags = True

    def get_search_fields(self, request):
        search_fields = list(super(
            CommissioneConsigliareAdmin, self).get_search_fields(request))
        for field in ['boss', 'vice', 'componenti']:
            search_fields += ['{}__persona__cognome'.format(field),
                              '{}__persona__nome'.format(field)]
        return tuple(set(search_fields))
