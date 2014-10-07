# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib import admin

from .models import (Ente, Mandato, Persona, GruppoConsigliare, Assessore,
                     Consigliere)


RANGE_VALIDITA_SECTION = ('Range di validità',
                          {'fields': ('inizio_validita', 'fine_validita')})


class GruppoConsigliareInline(admin.TabularInline):
    fields = ('nome',)
    model = GruppoConsigliare
    extra = 1


class AssessoreInline(admin.TabularInline):
    fields = ('persona', 'delega')
    model = Assessore
    extra = 1


class ConsigliereInline(admin.TabularInline):
    fields = ('persona', 'gruppoconsigliare')
    model = Consigliere
    extra = 1


@admin.register(Persona)
class PersonaAdmin(admin.ModelAdmin):
    fieldsets = (
        ('None', {'fields': ('cognome', 'nome', 'ente', 'user')}),
        RANGE_VALIDITA_SECTION)
    list_display = ('cognome', 'nome', 'ente', 'user')


@admin.register(Ente)
class EnteAdmin(admin.ModelAdmin):
    fieldsets = (
        ('None', {'fields': ('nome', 'ente_padre')}),
        RANGE_VALIDITA_SECTION)
    list_display = ('nome', 'ente_padre')


@admin.register(Mandato)
class MandatoAdmin(admin.ModelAdmin):
    fieldsets = (
        ('None', {'fields': ('ente', 'boss', 'vice', 'speacker')}),
        RANGE_VALIDITA_SECTION)
    list_display = ('ente', 'inizio_validita', 'fine_validita', 'boss', 'vice',
                    'speacker')
    list_select_related = True
    inlines = [GruppoConsigliareInline, AssessoreInline, ConsigliereInline]


