# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0031_auto_20161007_1952'),
    ]

    operations = [
        migrations.AddField(
            model_name='intranetmeta',
            name='image_upload_allowed',
            field=models.BooleanField(default=True, verbose_name=b'Alle User d\xc3\xbcrfen Bilder hochladen?'),
        ),
        migrations.AddField(
            model_name='intranetmeta',
            name='video_upload_allowed',
            field=models.BooleanField(default=True, verbose_name=b'Alle User d\xc3\xbcrfen Videos hochladen?'),
        ),
        migrations.AlterField(
            model_name='match',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime.now, null=True, verbose_name=b'Startzeit', blank=True),
        ),
    ]
