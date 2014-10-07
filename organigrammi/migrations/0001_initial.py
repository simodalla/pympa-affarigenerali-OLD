# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Assessore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('created', model_utils.fields.AutoCreatedField(verbose_name='created', editable=False, default=django.utils.timezone.now)),
                ('modified', model_utils.fields.AutoLastModifiedField(verbose_name='modified', editable=False, default=django.utils.timezone.now)),
                ('inizio_validita', models.DateTimeField(verbose_name='Data inizio validita', default=django.utils.timezone.now)),
                ('fine_validita', models.DateTimeField(null=True, blank=True, verbose_name='Data fine validita')),
                ('delega', models.CharField(max_length=500)),
            ],
            options={
                'verbose_name': 'Assessore',
                'verbose_name_plural': 'Assessori',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Consigliere',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('created', model_utils.fields.AutoCreatedField(verbose_name='created', editable=False, default=django.utils.timezone.now)),
                ('modified', model_utils.fields.AutoLastModifiedField(verbose_name='modified', editable=False, default=django.utils.timezone.now)),
                ('inizio_validita', models.DateTimeField(verbose_name='Data inizio validita', default=django.utils.timezone.now)),
                ('fine_validita', models.DateTimeField(null=True, blank=True, verbose_name='Data fine validita')),
            ],
            options={
                'verbose_name': 'Consigliere',
                'verbose_name_plural': 'Consiglieri',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('created', model_utils.fields.AutoCreatedField(verbose_name='created', editable=False, default=django.utils.timezone.now)),
                ('modified', model_utils.fields.AutoLastModifiedField(verbose_name='modified', editable=False, default=django.utils.timezone.now)),
                ('inizio_validita', models.DateTimeField(verbose_name='Data inizio validita', default=django.utils.timezone.now)),
                ('fine_validita', models.DateTimeField(null=True, blank=True, verbose_name='Data fine validita')),
                ('nome', models.CharField(unique=True, max_length=200)),
                ('ente_padre', models.ForeignKey(null=True, to='organigrammi.Ente', blank=True)),
            ],
            options={
                'verbose_name': 'Ente',
                'verbose_name_plural': 'Enti',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GruppoConsigliare',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('created', model_utils.fields.AutoCreatedField(verbose_name='created', editable=False, default=django.utils.timezone.now)),
                ('modified', model_utils.fields.AutoLastModifiedField(verbose_name='modified', editable=False, default=django.utils.timezone.now)),
                ('inizio_validita', models.DateTimeField(verbose_name='Data inizio validita', default=django.utils.timezone.now)),
                ('fine_validita', models.DateTimeField(null=True, blank=True, verbose_name='Data fine validita')),
                ('nome', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Gruppo Consigliare',
                'verbose_name_plural': 'Gruppo Consigliari',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Mandato',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('created', model_utils.fields.AutoCreatedField(verbose_name='created', editable=False, default=django.utils.timezone.now)),
                ('modified', model_utils.fields.AutoLastModifiedField(verbose_name='modified', editable=False, default=django.utils.timezone.now)),
                ('data_inizio', models.DateField()),
                ('data_fine', models.DateField()),
            ],
            options={
                'verbose_name': 'Mandato',
                'verbose_name_plural': 'Mandati',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('created', model_utils.fields.AutoCreatedField(verbose_name='created', editable=False, default=django.utils.timezone.now)),
                ('modified', model_utils.fields.AutoLastModifiedField(verbose_name='modified', editable=False, default=django.utils.timezone.now)),
                ('inizio_validita', models.DateTimeField(verbose_name='Data inizio validita', default=django.utils.timezone.now)),
                ('fine_validita', models.DateTimeField(null=True, blank=True, verbose_name='Data fine validita')),
                ('cognome', models.CharField(verbose_name='Cognome', max_length=80)),
                ('nome', models.CharField(verbose_name='Nome', max_length=80)),
                ('ente', models.ForeignKey(null=True, to='organigrammi.Ente', blank=True)),
                ('user', models.OneToOneField(null=True, to=settings.AUTH_USER_MODEL, blank=True, verbose_name='Utente del sistema')),
            ],
            options={
                'verbose_name': 'Persona',
                'verbose_name_plural': 'Persone',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='mandato',
            name='boss',
            field=models.OneToOneField(null=True, to='organigrammi.Persona', blank=True, verbose_name="Sindaco o Presidente dell'unione", related_name='boss_mandato'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='mandato',
            name='ente',
            field=models.ForeignKey(to='organigrammi.Ente'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='mandato',
            name='speacker',
            field=models.OneToOneField(null=True, to='organigrammi.Persona', blank=True, verbose_name='Presidente del consiglio', related_name='speacker_mandato'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='mandato',
            name='vice',
            field=models.OneToOneField(null=True, to='organigrammi.Persona', blank=True, verbose_name="Vicesindaco o Vicepresidente  dell'unione", related_name='vice_mandato'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gruppoconsigliare',
            name='mandato',
            field=models.ForeignKey(to='organigrammi.Mandato'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='consigliere',
            name='gruppoconsigliare',
            field=models.ForeignKey(null=True, to='organigrammi.GruppoConsigliare', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='consigliere',
            name='mandato',
            field=models.ForeignKey(to='organigrammi.Mandato'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='consigliere',
            name='persona',
            field=models.ForeignKey(to='organigrammi.Persona'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='assessore',
            name='mandato',
            field=models.ForeignKey(to='organigrammi.Mandato'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='assessore',
            name='persona',
            field=models.OneToOneField(to='organigrammi.Persona'),
            preserve_default=True,
        ),
    ]
