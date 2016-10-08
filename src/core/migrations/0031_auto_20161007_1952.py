# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0030_userextension_participated_lans'),
    ]

    operations = [
        migrations.CreateModel(
            name='Software',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name=b'Name')),
                ('file', models.FileField(upload_to=b'software', verbose_name=b'Dateiupload')),
                ('description', models.TextField(max_length=255, null=True, verbose_name=b'Beschreibung', blank=True)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Software',
                'verbose_name_plural': 'Software',
            },
        ),
        migrations.AlterField(
            model_name='match',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2016, 10, 7, 19, 52, 49, 193521), null=True, verbose_name=b'Startzeit', blank=True),
        ),
    ]
