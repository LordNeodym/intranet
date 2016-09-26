# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_auto_20160926_2246'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='lan',
            field=models.ForeignKey(related_name='match_lan', default=1, verbose_name=b'LAN', to='core.IntranetMeta'),
        ),
        migrations.AlterField(
            model_name='intranetmeta',
            name='lan_id',
            field=models.PositiveIntegerField(unique=True, verbose_name=b'LAN ID'),
        ),
    ]
