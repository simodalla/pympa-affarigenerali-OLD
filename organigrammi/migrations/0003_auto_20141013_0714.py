# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organigrammi', '0002_auto_20141010_1509'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sessioneassemblea',
            options={'ordering': ('data_svolgimento',), 'verbose_name_plural': 'Sessioni Assemblea', 'verbose_name': 'Sessione Assemblea'},
        ),
        migrations.RenameField(
            model_name='commissioneconsigliare',
            old_name='componenti',
            new_name='consiglieri',
        ),
        migrations.AlterField(
            model_name='assessore',
            name='mandato',
            field=models.ForeignKey(to='organigrammi.Mandato', related_name='assessori'),
        ),
        migrations.AlterField(
            model_name='consigliere',
            name='mandato',
            field=models.ForeignKey(to='organigrammi.Mandato', related_name='consiglieri'),
        ),
    ]
