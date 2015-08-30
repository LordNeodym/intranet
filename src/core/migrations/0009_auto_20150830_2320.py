# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_match_datetime'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='match',
            options={'ordering': ['game', 'datetime'], 'verbose_name': 'Match', 'verbose_name_plural': 'Matches'},
        ),
        migrations.AlterModelOptions(
            name='round',
            options={'ordering': ['round_number', 'datetime'], 'verbose_name': 'Runde', 'verbose_name_plural': 'Runden'},
        ),
        migrations.RemoveField(
            model_name='round',
            name='date',
        ),
        migrations.RemoveField(
            model_name='round',
            name='time',
        ),
        migrations.AddField(
            model_name='round',
            name='datetime',
            field=models.DateTimeField(null=True, verbose_name=b'Datum/Uhrzeit', blank=True),
        ),
        migrations.AlterField(
            model_name='round',
            name='pkt1',
            field=models.IntegerField(null=True, verbose_name=b'Punkte Heim', blank=True),
        ),
        migrations.AlterField(
            model_name='round',
            name='pkt2',
            field=models.IntegerField(null=True, verbose_name=b'Punkte Gast', blank=True),
        ),
    ]
