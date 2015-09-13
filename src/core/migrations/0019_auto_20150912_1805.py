# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_auto_20150910_1350'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='description',
            field=models.TextField(max_length=1024, null=True, verbose_name=b'Beschreibung / Installationsanleitung', blank=True),
        ),
        migrations.AlterField(
            model_name='match',
            name='team_choose_type',
            field=models.CharField(default=b'None', max_length=5, verbose_name=b'Team Wahl', blank=True, choices=[(b'None', b'Bitte w\xc3\xa4hlen'), (b'rand', b'Zufalls Wahl'), (b'self', b'Eigene Wahl'), (b'admin', b'Admin Wahl')]),
        ),
    ]
