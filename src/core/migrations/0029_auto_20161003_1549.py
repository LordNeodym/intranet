# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_auto_20160928_0031'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='intranetmeta',
            options={'ordering': ['-lan_id'], 'verbose_name': 'Intranet Metadaten', 'verbose_name_plural': 'Intranet Metadaten'},
        ),
        migrations.AddField(
            model_name='userextension',
            name='ip',
            field=models.GenericIPAddressField(null=True, verbose_name=b'IP-Adresse', blank=True),
        ),
        migrations.AddField(
            model_name='userextension',
            name='seat',
            field=models.CharField(max_length=63, null=True, verbose_name=b'Sitzplatz', blank=True),
        ),
        migrations.AlterField(
            model_name='match',
            name='lan',
            field=models.ForeignKey(related_name='match_lan', verbose_name=b'LAN', to='core.IntranetMeta'),
        ),
    ]
