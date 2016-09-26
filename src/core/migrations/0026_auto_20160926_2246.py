# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_auto_20160924_1740'),
    ]

    operations = [
        migrations.AddField(
            model_name='intranetmeta',
            name='date',
            field=models.DateField(default=datetime.datetime(2016, 9, 26, 20, 45, 59, 607728, tzinfo=utc), verbose_name=b'Beginn der LAN'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='intranetmeta',
            name='lan_id',
            field=models.PositiveIntegerField(default=5, verbose_name=b'LAN ID'),
            preserve_default=False,
        ),
    ]
