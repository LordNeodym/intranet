# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
                ('game_mode', models.CharField(max_length=50, null=True, verbose_name=b'Modus', blank=True)),
                ('player_per_team', models.IntegerField(verbose_name=b'Spieler pro Team')),
                ('description', models.CharField(max_length=255, null=True, verbose_name=b'Beschreibung', blank=True)),
                ('game', models.ForeignKey(related_name='match_game', verbose_name=b'Spiel', to='core.Game')),
                ('user', models.ForeignKey(related_name='match_user', verbose_name=b'Spieler', to=settings.AUTH_USER_MODEL)),
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
                ('pkt1', models.IntegerField(verbose_name=b'Punkte Heim')),
                ('pkt2', models.IntegerField(verbose_name=b'Punkte Gast')),
                ('date', models.DateField(null=True, verbose_name=b'Datum', blank=True)),
                ('time', models.TimeField(null=True, verbose_name=b'Uhrzeit', blank=True)),
            ],
            options={
                'ordering': ['round_number'],
                'verbose_name': 'Runde',
                'verbose_name_plural': 'Runden',
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=50, null=True, verbose_name=b'Teamname', blank=True)),
                ('match', models.ForeignKey(related_name='team_match', verbose_name=b'Match', to='core.Match')),
                ('user', models.ForeignKey(related_name='team_user', verbose_name=b'Spieler', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Team',
                'verbose_name_plural': 'Teams',
            },
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
