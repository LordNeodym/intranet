# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_intranetmeta_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rules',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'Allgemeine Regeln', unique=True, max_length=30, verbose_name=b'Regelgruppe')),
                ('slug', models.SlugField(editable=False, blank=True, unique=True, verbose_name=b'Slug')),
            ],
            options={
                'verbose_name': 'Regelgruppe',
                'verbose_name_plural': 'Regelgruppen',
            },
        ),
        migrations.CreateModel(
            name='RulesInline',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('information', models.TextField(max_length=512, null=True, verbose_name=b'Regel', blank=True)),
                ('rules', models.ForeignKey(related_name='inline_rules', verbose_name=b'Regelgruppe', blank=True, to='core.Rules', null=True)),
            ],
            options={
                'verbose_name': 'Regel',
                'verbose_name_plural': 'Regeln',
            },
        ),
        migrations.AlterField(
            model_name='game',
            name='slug',
            field=models.SlugField(editable=False, blank=True, unique=True, verbose_name=b'Slug'),
        ),
    ]
