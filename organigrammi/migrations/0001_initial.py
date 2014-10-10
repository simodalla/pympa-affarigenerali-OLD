# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import model_utils.fields
from django.conf import settings
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Assessore',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(editable=False, default=django.utils.timezone.now, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(editable=False, default=django.utils.timezone.now, verbose_name='modified')),
                ('inizio_validita', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Data inizio validita')),
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
            name='CommissioneConsigliare',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(editable=False, default=django.utils.timezone.now, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(editable=False, default=django.utils.timezone.now, verbose_name='modified')),
                ('titolo', models.CharField(max_length=500)),
            ],
            options={
                'verbose_name': 'Commissione Consigliare',
                'verbose_name_plural': 'Commissioni Consigliari',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Consigliere',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(editable=False, default=django.utils.timezone.now, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(editable=False, default=django.utils.timezone.now, verbose_name='modified')),
                ('inizio_validita', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Data inizio validita')),
                ('fine_validita', models.DateTimeField(null=True, blank=True, verbose_name='Data fine validita')),
                ('capogruppo', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Consigliere',
                'verbose_name_plural': 'Consiglieri',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Consiglio',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(editable=False, default=django.utils.timezone.now, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(editable=False, default=django.utils.timezone.now, verbose_name='modified')),
            ],
            options={
                'verbose_name': 'Consiglio',
                'verbose_name_plural': 'Consigli',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ente',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(editable=False, default=django.utils.timezone.now, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(editable=False, default=django.utils.timezone.now, verbose_name='modified')),
                ('inizio_validita', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Data inizio validita')),
                ('fine_validita', models.DateTimeField(null=True, blank=True, verbose_name='Data fine validita')),
                ('titolo', models.CharField(max_length=200, unique=True)),
                ('ente_padre', models.ForeignKey(null=True, blank=True, to='organigrammi.Ente')),
            ],
            options={
                'verbose_name': 'Ente',
                'verbose_name_plural': 'Enti',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Giunta',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(editable=False, default=django.utils.timezone.now, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(editable=False, default=django.utils.timezone.now, verbose_name='modified')),
            ],
            options={
                'verbose_name': 'Giunta',
                'verbose_name_plural': 'Giunte',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GruppoConsigliare',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(editable=False, default=django.utils.timezone.now, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(editable=False, default=django.utils.timezone.now, verbose_name='modified')),
                ('inizio_validita', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Data inizio validita')),
                ('fine_validita', models.DateTimeField(null=True, blank=True, verbose_name='Data fine validita')),
                ('titolo', models.CharField(max_length=200)),
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
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(editable=False, default=django.utils.timezone.now, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(editable=False, default=django.utils.timezone.now, verbose_name='modified')),
                ('inizio_validita', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Data inizio validita')),
                ('fine_validita', models.DateTimeField(null=True, blank=True, verbose_name='Data fine validita')),
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
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(editable=False, default=django.utils.timezone.now, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(editable=False, default=django.utils.timezone.now, verbose_name='modified')),
                ('inizio_validita', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Data inizio validita')),
                ('fine_validita', models.DateTimeField(null=True, blank=True, verbose_name='Data fine validita')),
                ('cognome', models.CharField(max_length=80, verbose_name='Cognome')),
                ('nome', models.CharField(max_length=80, verbose_name='Nome')),
                ('email', models.EmailField(null=True, max_length=75, blank=True)),
                ('ente', models.ForeignKey(null=True, blank=True, to='organigrammi.Ente')),
                ('user', models.OneToOneField(verbose_name='Utente del sistema', null=True, blank=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Persona',
                'verbose_name_plural': 'Persone',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Presenza',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(editable=False, default=django.utils.timezone.now, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(editable=False, default=django.utils.timezone.now, verbose_name='modified')),
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
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(editable=False, default=django.utils.timezone.now, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(editable=False, default=django.utils.timezone.now, verbose_name='modified')),
                ('data_svolgimento', models.DateField()),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': 'Sessione Assembla',
                'verbose_name_plural': 'Sessioni Assembla',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='sessioneassembla',
            unique_together=set([('data_svolgimento', 'object_id', 'content_type')]),
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
            model_name='mandato',
            name='boss',
            field=models.OneToOneField(verbose_name="Sindaco o Presidente dell'unione", null=True, related_name='boss_mandato', blank=True, to='organigrammi.Persona'),
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
            field=models.OneToOneField(verbose_name='Presidente del consiglio', null=True, related_name='speacker_mandato', blank=True, to='organigrammi.Persona'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='mandato',
            name='vice',
            field=models.OneToOneField(verbose_name="Vicesindaco o Vicepresidente  dell'unione", null=True, related_name='vice_mandato', blank=True, to='organigrammi.Persona'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='mandato',
            name='vice_speacker',
            field=models.OneToOneField(verbose_name='Vicepresidente del consiglio', null=True, related_name='vicespeacker_mandato', blank=True, to='organigrammi.Persona'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gruppoconsigliare',
            name='mandato',
            field=models.ForeignKey(to='organigrammi.Mandato'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='giunta',
            name='mandato',
            field=models.OneToOneField(to='organigrammi.Mandato'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='consiglio',
            name='mandato',
            field=models.OneToOneField(to='organigrammi.Mandato'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='consigliere',
            name='gruppoconsigliare',
            field=models.ForeignKey(null=True, blank=True, to='organigrammi.GruppoConsigliare'),
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
            model_name='commissioneconsigliare',
            name='boss',
            field=models.OneToOneField(verbose_name='Presidente della commissione', null=True, related_name='boss_commissione', blank=True, to='organigrammi.Consigliere'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='commissioneconsigliare',
            name='componenti',
            field=models.ManyToManyField(null=True, to='organigrammi.Consigliere', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='commissioneconsigliare',
            name='mandato',
            field=models.ForeignKey(to='organigrammi.Mandato'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='commissioneconsigliare',
            name='vice',
            field=models.OneToOneField(verbose_name='Vicepresidente della commissione', null=True, related_name='vice_commisione', blank=True, to='organigrammi.Consigliere'),
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
