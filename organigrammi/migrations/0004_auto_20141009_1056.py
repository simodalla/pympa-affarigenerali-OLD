# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organigrammi', '0003_auto_20141008_1131'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ente',
            old_name='nome',
            new_name='titolo',
        ),
        migrations.RenameField(
            model_name='gruppoconsigliare',
            old_name='nome',
            new_name='titolo',
        ),
        migrations.AddField(
            model_name='commissioneconsigliare',
            name='titolo',
            field=models.CharField(default='commissione', max_length=500),
            preserve_default=False,
        ),
    ]
