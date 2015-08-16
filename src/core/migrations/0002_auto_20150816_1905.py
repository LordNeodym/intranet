# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='round',
            name='date',
            field=models.DateField(null=True, verbose_name=b'Datum', blank=True),
        ),
        migrations.AddField(
            model_name='round',
            name='time',
            field=models.TimeField(null=True, verbose_name=b'Uhrzeit', blank=True),
        ),
        migrations.AlterField(
            model_name='match',
            name='game_mode',
            field=models.CharField(max_length=50, null=True, verbose_name=b'Modus', blank=True),
        ),
    ]
