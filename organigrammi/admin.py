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
        ('None', {'fields': ('cognome', 'nome', 'email', 'ente', 'user')}),
        RANGE_VALIDITA_SECTION)
    list_display = ('cognome', 'nome', 'ente', 'user', 'inizio_validita',
                    'fine_validita')


@admin.register(Ente)
class EnteAdmin(admin.ModelAdmin):
    fieldsets = (
        ('None', {'fields': ('titolo', 'ente_padre')}),
        RANGE_VALIDITA_SECTION)
    list_display = ('titolo', 'ente_padre')


@admin.register(Mandato)
class MandatoAdmin(admin.ModelAdmin):
    fieldsets = (
        ('None', {'fields': ('ente', 'boss', 'vice', 'speacker',
                             'vice_speacker')}),
        RANGE_VALIDITA_SECTION)
    list_display = ('ente', 'inizio_validita', 'fine_validita', 'boss', 'vice',
                    'speacker')
    list_select_related = True
    inlines = [AssessoreInline, GruppoConsigliareInline, ConsigliereInline]


@admin.register(CommissioneConsigliare)
class CommissioneConsigliareAdmin(admin.ModelAdmin):
    fieldsets = (
        ('None', {'fields': ('mandato', 'titolo', 'boss', 'vice',
                             'componenti')}),
    )
    filter_horizontal = ('componenti',)
    list_display = ('mandato', 'boss', 'vice',)

    def ld_componenti(self, obj):
        """
        :type obj: organigrammi.models.CommissioneConsigliare
        """
        links = ['<a href="{}">{}</a>'.format(
            c.get_absolute_url()) for c in obj.componenti]
        return '<br />'.join(links)
    ld_componenti.short_description = 'Componenti'
    ld_componenti.allow_tags = True