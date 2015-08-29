# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20150827_2320'),
    ]

    operations = [
        migrations.CreateModel(
            name='MatchRulesInline',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('information', models.TextField(max_length=512, null=True, verbose_name=b'Regel', blank=True)),
                ('match', models.ForeignKey(related_name='inline_rules', verbose_name=b'Spielregeln', blank=True, to='core.Match', null=True)),
            ],
            options={
                'verbose_name': 'Spielregel',
                'verbose_name_plural': 'Spielregeln',
            },
        ),
    ]
