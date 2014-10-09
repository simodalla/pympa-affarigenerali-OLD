# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organigrammi', '0004_auto_20141009_1056'),
    ]

    operations = [
        migrations.AddField(
            model_name='mandato',
            name='vice_speacker',
            field=models.OneToOneField(verbose_name='Vicepresidente del consiglio', to='organigrammi.Persona', blank=True, null=True, related_name='vicespeacker_mandato'),
            preserve_default=True,
        ),
    ]
