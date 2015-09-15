# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_auto_20150913_2108'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='tour_choose_type',
            field=models.CharField(default=b'None', editable=False, choices=[(b'None', b'Bitte w\xc3\xa4hlen'), (b'vs', b'Jeder gegen Jeden'), (b'tree', b'Turnierbaum'), (b'tree_loser', b'Turnierbaum mit Loserbracket')], max_length=10, blank=True, verbose_name=b'Turnier Wahl'),
        ),
        migrations.AlterField(
            model_name='match',
            name='team_choose_type',
            field=models.CharField(default=b'None', editable=False, choices=[(b'None', b'Bitte w\xc3\xa4hlen'), (b'rand', b'Zufalls Wahl'), (b'self', b'Eigene Wahl'), (b'admin', b'Admin Wahl')], max_length=5, blank=True, verbose_name=b'Team Wahl'),
        ),
        migrations.AlterField(
            model_name='round',
            name='team1',
            field=models.ForeignKey(related_name='round_team1', verbose_name=b'Team Heim', blank=True, to='core.Team', null=True),
        ),
        migrations.AlterField(
            model_name='round',
            name='team2',
            field=models.ForeignKey(related_name='round_team2', verbose_name=b'Team Gast', blank=True, to='core.Team', null=True),
        ),
    ]
