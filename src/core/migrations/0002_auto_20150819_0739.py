# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='user',
        ),
        migrations.AddField(
            model_name='match',
            name='user',
            field=models.ManyToManyField(related_name='match_user', verbose_name=b'Spieler', to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='team',
            name='user',
        ),
        migrations.AddField(
            model_name='team',
            name='user',
            field=models.ManyToManyField(related_name='team_user', verbose_name=b'Spieler', to=settings.AUTH_USER_MODEL),
        ),
    ]
