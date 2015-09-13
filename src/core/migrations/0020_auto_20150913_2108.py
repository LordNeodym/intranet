# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_auto_20150912_1805'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='matchrulesinline',
            name='match',
        ),
        migrations.AddField(
            model_name='match',
            name='rules',
            field=models.TextField(max_length=1024, null=True, verbose_name=b'Spielregeln', blank=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='name',
            field=models.CharField(unique=True, max_length=30, verbose_name=b'Name'),
        ),
        migrations.DeleteModel(
            name='MatchRulesInline',
        ),
    ]
