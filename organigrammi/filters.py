# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import pyclbr

from django.contrib.admin import SimpleListFilter
from django.contrib.contenttypes.models import ContentType


class FilterContentTypeListFilter(SimpleListFilter):
    title = 'tipo di assemblea'
    parameter_name = 'sessione__content_type'

    parent_class = ['Assemblea']

    def lookups(self, request, model_admin):
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