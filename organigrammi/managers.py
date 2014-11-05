# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.db.models import Manager, Q
from django.utils.timezone import now


class RangeValiditaManager(Manager):

    # def validi_tra(self, inizio_validita, fine_validita=None):

    def validi(self):
        return self.filter(
            Q(inizio_validita__lte=now()),
            Q(fine_validita__gte=now()) | Q(fine_validita__isnull=True),)