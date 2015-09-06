# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20150902_2137'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='team_choose_type',
            field=models.CharField(default=b'None', max_length=5, verbose_name=b'Team Wahl', choices=[(b'rand', b'Zufall'), (b'self', b'Eigene Wahl'), (b'admin', b'Admin Wahl')]),
        ),
    ]
