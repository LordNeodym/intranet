# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20150829_2047'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='datetime',
            field=models.DateTimeField(null=True, verbose_name=b'Datum/Uhrzeit', blank=True),
        ),
    ]
