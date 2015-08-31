# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_match_datetime'),
    ]

    operations = [
        migrations.CreateModel(
            name='Round',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('round_number', models.IntegerField(null=True, verbose_name=b'Rundennummer', blank=True)),
                ('pkt1', models.IntegerField(null=True, verbose_name=b'Punkte Heim', blank=True)),
                ('pkt2', models.IntegerField(null=True, verbose_name=b'Punkte Gast', blank=True)),
                ('datetime', models.DateTimeField(null=True, verbose_name=b'Datum/Uhrzeit', blank=True)),
            ],
            options={
                'ordering': ['round_number', 'datetime'],
                'verbose_name': 'Runde',
                'verbose_name_plural': 'Runden',
            },
        ),
        migrations.AlterModelOptions(
            name='match',
            options={'ordering': ['game', 'datetime'], 'verbose_name': 'Match', 'verbose_name_plural': 'Matches'},
        ),
        migrations.AddField(
            model_name='round',
            name='match',
            field=models.ForeignKey(verbose_name=b'Match', to='core.Match'),
        ),
        migrations.AddField(
            model_name='round',
            name='team1',
            field=models.ForeignKey(related_name='round_team1', verbose_name=b'Team Heim', to='core.Team'),
        ),
        migrations.AddField(
            model_name='round',
            name='team2',
            field=models.ForeignKey(related_name='round_team2', verbose_name=b'Team Gast', to='core.Team'),
        ),
    ]
