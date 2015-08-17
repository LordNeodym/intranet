# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0002_auto_20150816_1905'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=50, null=True, verbose_name=b'Teamname', blank=True)),
                ('user', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name=b'Spieler')),
            ],
            options={
                'verbose_name': 'Team',
                'verbose_name_plural': 'Teams',
            },
        ),
        migrations.CreateModel(
            name='TeamRound',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pts', models.IntegerField(null=True, verbose_name=b'Punkte', blank=True)),
                ('match', models.ForeignKey(verbose_name=b'Match', to='core.Match')),
            ],
            options={
                'ordering': ['match', 'round', 'pts'],
                'verbose_name': 'TeamRunde',
                'verbose_name_plural': 'TeamRunden',
            },
        ),
        migrations.AlterModelOptions(
            name='round',
            options={'ordering': ['round_number'], 'verbose_name': 'Runde', 'verbose_name_plural': 'Runden'},
        ),
        migrations.RemoveField(
            model_name='round',
            name='match',
        ),
        migrations.RemoveField(
            model_name='round',
            name='pts_away',
        ),
        migrations.RemoveField(
            model_name='round',
            name='pts_home',
        ),
        migrations.AddField(
            model_name='teamround',
            name='round',
            field=models.ForeignKey(verbose_name=b'Runde', to='core.Round'),
        ),
        migrations.AddField(
            model_name='teamround',
            name='team',
            field=models.ForeignKey(verbose_name=b'Team', to='core.Team'),
        ),
    ]
