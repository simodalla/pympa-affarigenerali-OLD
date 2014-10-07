# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('organigrammi', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mandato',
            name='data_fine',
        ),
        migrations.RemoveField(
            model_name='mandato',
            name='data_inizio',
        ),
        migrations.AddField(
            model_name='mandato',
            name='fine_validita',
            field=models.DateTimeField(blank=True, verbose_name='Data fine validita', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='mandato',
            name='inizio_validita',
            field=models.DateTimeField(verbose_name='Data inizio validita', default=django.utils.timezone.now),
            preserve_default=True,
        ),
    ]
