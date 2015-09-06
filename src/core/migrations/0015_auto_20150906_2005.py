# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filer.fields.image


class Migration(migrations.Migration):

    dependencies = [
        ('filer', '0002_auto_20150606_2003'),
        ('core', '0014_match_team_choose_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='img',
        ),
        migrations.AddField(
            model_name='game',
            name='icon',
            field=filer.fields.image.FilerImageField(related_name='game_icon', verbose_name=b'Icon', blank=True, to='filer.Image', null=True),
        ),
        migrations.AlterField(
            model_name='match',
            name='team_choose_type',
            field=models.CharField(default=b'None', max_length=5, verbose_name=b'Team Wahl', choices=[(b'None', b'Bitte w\xc3\xa4hlen'), (b'rand', b'Zufalls Wahl'), (b'self', b'Eigene Wahl'), (b'admin', b'Admin Wahl')]),
        ),
    ]
