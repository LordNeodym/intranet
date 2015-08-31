# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20150831_2238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='round',
            name='match',
            field=models.ForeignKey(related_name='round_match', verbose_name=b'Match', to='core.Match'),
        ),
    ]
