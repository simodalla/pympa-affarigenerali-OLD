# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import model_utils.fields
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('organigrammi', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SessioneAssemblea',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('data_svolgimento', models.DateField()),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name_plural': 'Sessioni Assemblea',
                'verbose_name': 'Sessione Assemblea',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='sessioneassembla',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='sessioneassembla',
            name='content_type',
        ),
        migrations.AlterUniqueTogether(
            name='sessioneassemblea',
            unique_together=set([('data_svolgimento', 'object_id', 'content_type')]),
        ),
        migrations.AlterField(
            model_name='presenza',
            name='sessione',
            field=models.ForeignKey(to='organigrammi.SessioneAssemblea'),
        ),
        migrations.DeleteModel(
            name='SessioneAssembla',
        ),
    ]
