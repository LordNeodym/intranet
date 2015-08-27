# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20150827_2029'),
    ]

    operations = [
        migrations.AddField(
            model_name='intranetmeta',
            name='title',
            field=models.CharField(default=b'Herzlich Willkommen im Intranet', max_length=128, null=True, verbose_name=b'Begr\xc3\xbc\xc3\x9fungstext', blank=True),
        ),
    ]
