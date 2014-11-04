# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from calendar import month

from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.core.urlresolvers import reverse

from .models import (Ente, Mandato, Persona, GruppoConsigliare, Assessore,
                     Consigliere, SessioneAssemblea, CommissioneConsigliare,
                     Consiglio, Giunta, Presenza)


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


class PresenzaInline(admin.TabularInline):
    model = Presenza
    extra = 1

    def has_delete_permission(self, request, obj=None):
        return False


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


class SessioneAssembleaInline(GenericTabularInline):
    model = SessioneAssemblea


class SessioneAssembleaAdminMixin():
    inlines = [SessioneAssembleaInline]

    def ld_sessioni_assemblea(self, obj):
        """
        :type obj: organigrammi.models.CommissioneConsigliare
        """
        return '<br />'.join(
            ['{}&nbsp;<a href="{}">presenze'
             '</a>'.format(c, reverse(admin_urlname(c._meta, 'change'),
                                      args=(c.pk,)))
             for c in obj.sessioni.all()])
    ld_sessioni_assemblea.short_description = 'Sessioni'
    ld_sessioni_assemblea.allow_tags = True

    def ld_componenti(self, obj):
        """
        :type obj: organigrammi.models.CommissioneConsigliare
        """
        links = ['<a href="{}">{}</a>'.format(url, label)
                 for url, label in obj.ld_componenti]
        return '<br />'.join(links)
    ld_componenti.short_description = 'Componenti'
    ld_componenti.allow_tags = True


@admin.register(CommissioneConsigliare)
class CommissioneConsigliareAdmin(SessioneAssembleaAdminMixin,
                                  admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('mandato', 'titolo', 'boss', 'vice',
                           'consiglieri',)}),
    )
    filter_horizontal = ('consiglieri', )
    list_display = ('titolo', 'mandato', 'ld_componenti',
                    'ld_sessioni_assemblea')
    list_filter = ('mandato',)
    list_select_related = True
    search_fields = ('titolo', 'mandato__ente__titolo',)

    def get_search_fields(self, request):
        search_fields = list(super(
            CommissioneConsigliareAdmin, self).get_search_fields(request))
        for field in ['boss', 'vice', 'consiglieri']:
            search_fields += ['{}__persona__cognome'.format(field),
                              '{}__persona__nome'.format(field)]
        return tuple(set(search_fields))


@admin.register(Consiglio)
class ConsiglioAdmin(SessioneAssembleaAdminMixin, admin.ModelAdmin):
    list_display = ('mandato', 'ld_componenti', 'ld_sessioni_assemblea')


@admin.register(Giunta)
class GiuntaAdmin(SessioneAssembleaAdminMixin, admin.ModelAdmin):
    list_display = ('mandato', 'ld_componenti', 'ld_sessioni_assemblea')


@admin.register(SessioneAssemblea)
class SessioneAssembleaAdmin(admin.ModelAdmin):
    date_hierarchy = 'data_svolgimento'
    inlines = [PresenzaInline]
    list_display = ('data_svolgimento', 'content_type')
    list_filter = ('content_type',)
    readonly_fields = ('data_svolgimento', 'content_type', 'object_id')

    def has_add_permission(self, request):
        return False

    def change_view(self, request, object_id, *args, **kwargs):
        sessione = SessioneAssemblea.objects.get(pk=object_id)
        if sessione.presenze.count() == 0:
            sessione.create_presenze_of_componenti()
        return super(SessioneAssembleaAdmin, self).change_view(
            request, object_id, *args, **kwargs)


class FilterContentTypeListFilter(admin.SimpleListFilter):
    title = 'tipo di assemblea'
    parameter_name = 'sessione__content_type'

    parent_class = ['Assemblea']

    def lookups(self, request, model_admin):
        import pyclbr
        models_classes = pyclbr.readmodule('organigrammi.models')
        parent_childs = [
            c.lower() for c in models_classes
            if set(self.parent_class).intersection(
                set([o.name for o in models_classes[c].super
                     if isinstance(o, pyclbr.Class)]))]
        return tuple((ct.pk, ct.name) for ct in
                     ContentType.objects.filter(app_label='organigrammi',
                                                model__in=parent_childs))

    def queryset(self, request, queryset):
        if self.value():
            queryset = queryset.filter(**{self.parameter_name: self.value()})
        return queryset



@admin.register(Presenza)
class PresenzaAdmin(admin.ModelAdmin):
    list_display = ('id', 'persona', 'sessione', 'presenza')
    list_filter = (FilterContentTypeListFilter, 'persona')
    search_fields = ('persona__cognome', 'persona__nome')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        if obj:
            return False
        return super(PresenzaAdmin, self).has_change_permission(request, obj)

    def get_urls(self):
        from django.conf.urls import patterns, url
        from .views import RiepiloghiPresenzeView
        import datetime
        today = datetime.date.today()
        first_of_year = datetime.date(year=today.year, month=1, day=1)
        my_urls = patterns(
            '',
            url(r'^riepiloghi/$',
                self.admin_site.admin_view(RiepiloghiPresenzeView.as_view()),
                name='organigrammi_presenza_visualizzazione',
                kwargs={'from_year': first_of_year.year,
                        'from_month': first_of_year.month,
                        'from_day': first_of_year.day,
                        'to_year': today.year,
                        'to_month': today.month,
                        'to_day': today.day}),
            url(r'^riepiloghi/(?P<from_year>\d{4})/(?P<from_month>\d{2})/'
                r'(?P<from_day>\d{2})/(?P<to_year>\d{4})/(?P<to_month>\d{2})/'
                r'(?P<to_day>\d{2})/$',
                self.admin_site.admin_view(RiepiloghiPresenzeView.as_view()),
                name='organigrammi_presenza_visualizzazione')
        )
        return my_urls + super(PresenzaAdmin, self).get_urls()

    class Media:
        css = {
            "all": ("my_styles.css",)
        }
        # js = {
        #     "organigrammi_presenza_visualizzazione": ("my_code.js",)
        # }