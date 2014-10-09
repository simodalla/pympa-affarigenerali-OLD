# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('organigrammi', '0002_auto_20141007_1011'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assemblea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CommissioneConsigliare',
            fields=[
                ('assemblea_ptr', models.OneToOneField(auto_created=True, to='organigrammi.Assemblea', serialize=False, parent_link=True, primary_key=True)),
                ('boss', models.OneToOneField(related_name='boss_commissione', to='organigrammi.Consigliere', verbose_name='Presidente della commissione', blank=True, null=True)),
                ('componenti', models.ManyToManyField(to='organigrammi.Consigliere', blank=True, null=True)),
                ('vice', models.OneToOneField(related_name='vice_commisione', to='organigrammi.Consigliere', verbose_name='Vicepresidente della commissione', blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Commissione Consigliare',
                'verbose_name_plural': 'Commissioni Consigliari',
            },
            bases=('organigrammi.assemblea',),
        ),
        migrations.CreateModel(
            name='Consiglio',
            fields=[
                ('assemblea_ptr', models.OneToOneField(auto_created=True, to='organigrammi.Assemblea', serialize=False, parent_link=True, primary_key=True)),
            ],
            options={
                'verbose_name': 'Consiglio',
                'verbose_name_plural': 'Consigli',
            },
            bases=('organigrammi.assemblea',),
        ),
        migrations.CreateModel(
            name='Giunta',
            fields=[
                ('assemblea_ptr', models.OneToOneField(auto_created=True, to='organigrammi.Assemblea', serialize=False, parent_link=True, primary_key=True)),
            ],
            options={
                'verbose_name': 'Giunta',
                'verbose_name_plural': 'Giunte',
            },
            bases=('organigrammi.assemblea',),
        ),
        migrations.CreateModel(
            name='Presenza',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('presenza', models.BooleanField(default=False)),
                ('persona', models.ForeignKey(to='organigrammi.Persona')),
            ],
            options={
                'verbose_name': 'Presenza',
                'verbose_name_plural': 'Presenze',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SessioneAssembla',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('data_svolgimento', models.DateField()),
            ],
            options={
                'verbose_name': 'Sessione Assembla',
                'verbose_name_plural': 'Sessioni Assembla',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SessioneCommissioneConsigliare',
            fields=[
                ('sessioneassembla_ptr', models.OneToOneField(auto_created=True, to='organigrammi.SessioneAssembla', serialize=False, parent_link=True, primary_key=True)),
            ],
            options={
                'verbose_name': 'Sessione di Commissione Consigliare',
                'verbose_name_plural': 'Sessioni di Commissione Consigliare',
            },
            bases=('organigrammi.sessioneassembla',),
        ),
        migrations.CreateModel(
            name='SessioneConsiglio',
            fields=[
                ('sessioneassembla_ptr', models.OneToOneField(auto_created=True, to='organigrammi.SessioneAssembla', serialize=False, parent_link=True, primary_key=True)),
            ],
            options={
                'verbose_name': 'Sessione di Consiglio',
                'verbose_name_plural': 'Sessioni di Consiglio',
            },
            bases=('organigrammi.sessioneassembla',),
        ),
        migrations.CreateModel(
            name='SessioneGiunta',
            fields=[
                ('sessioneassembla_ptr', models.OneToOneField(auto_created=True, to='organigrammi.SessioneAssembla', serialize=False, parent_link=True, primary_key=True)),
            ],
            options={
                'verbose_name': 'Sessione di Giunta',
                'verbose_name_plural': 'Sessioni di Giunta',
            },
            bases=('organigrammi.sessioneassembla',),
        ),
        migrations.AddField(
            model_name='sessioneassembla',
            name='assembla',
            field=models.ForeignKey(to='organigrammi.Assemblea'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='sessioneassembla',
            unique_together=set([('data_svolgimento', 'assembla')]),
        ),
        migrations.AddField(
            model_name='presenza',
            name='sessione',
            field=models.ForeignKey(to='organigrammi.SessioneAssembla'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='presenza',
            unique_together=set([('sessione', 'persona')]),
        ),
        migrations.AddField(
            model_name='assemblea',
            name='mandato',
            field=models.ForeignKey(to='organigrammi.Mandato'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='consigliere',
            name='capogruppo',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='persona',
            name='email',
            field=models.EmailField(max_length=75, blank=True, null=True),
            preserve_default=True,
        ),
    ]
