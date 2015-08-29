# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_matchrulesinline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='description',
            field=models.TextField(max_length=255, null=True, verbose_name=b'Beschreibung', blank=True),
        ),
    ]
