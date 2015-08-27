# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20150819_0739'),
    ]

    operations = [
        migrations.CreateModel(
            name='IntranetMeta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'Intranet', max_length=50, verbose_name=b'LAN Name')),
                ('description', models.TextField(max_length=1024, null=True, verbose_name=b'Beschreibung', blank=True)),
            ],
            options={
                'verbose_name': 'Intranet Metadaten',
                'verbose_name_plural': 'Intranet Metadaten',
            },
        ),
        migrations.AlterModelOptions(
            name='team',
            options={'ordering': ['description'], 'verbose_name': 'Team', 'verbose_name_plural': 'Teams'},
        ),
    ]
