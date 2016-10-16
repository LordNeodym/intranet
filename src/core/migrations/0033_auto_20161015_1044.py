# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0032_auto_20161008_1527'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuorder',
            name='creator',
            field=models.ForeignKey(default=1, verbose_name=b'Ersteller', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='menuorder',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name=b'Datum'),
        ),
    ]
