# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50, verbose_name=b'Name')),
                ('slug', models.SlugField(unique=True, verbose_name=b'Slug')),
                ('img', models.ImageField(upload_to=b'game_icon', null=True, verbose_name=b'Icon', blank=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Spiel',
                'verbose_name_plural': 'Spiele',
            },
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('game_mode', models.CharField(max_length=50, null=True, verbose_name=b'Gamemode', blank=True)),
                ('player_per_team', models.IntegerField(verbose_name=b'Spieler pro Team')),
                ('description', models.CharField(max_length=255, null=True, verbose_name=b'Beschreibung', blank=True)),
                ('game', models.ForeignKey(verbose_name=b'Spiel', to='core.Game')),
            ],
            options={
                'ordering': ['game', 'player_per_team'],
                'verbose_name': 'Match',
                'verbose_name_plural': 'Matches',
            },
        ),
        migrations.CreateModel(
            name='Round',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('round_number', models.IntegerField(null=True, verbose_name=b'Rundennummer', blank=True)),
                ('pts_home', models.IntegerField(verbose_name=b'Punkte Heim')),
                ('pts_away', models.IntegerField(verbose_name=b'Punkte Gast')),
                ('match', models.ForeignKey(verbose_name=b'Match', to='core.Match')),
            ],
            options={
                'ordering': ['match', 'round_number'],
                'verbose_name': 'Runde',
                'verbose_name_plural': 'Runden',
            },
        ),
    ]
