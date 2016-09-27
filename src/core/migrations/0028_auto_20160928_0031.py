# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_auto_20160927_0103'),
    ]

    operations = [
        migrations.AddField(
            model_name='intranetmeta',
            name='active',
            field=models.BooleanField(default=False, verbose_name=b'Aktiv?'),
        ),
        migrations.AlterField(
            model_name='match',
            name='player_per_team',
            field=models.IntegerField(verbose_name=b'Spieler pro Team', validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='match',
            name='user',
            field=models.ManyToManyField(related_name='match_user', verbose_name=b'Spieler', to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
