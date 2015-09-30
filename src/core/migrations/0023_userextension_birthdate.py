# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_auto_20150925_1543'),
    ]

    operations = [
        migrations.AddField(
            model_name='userextension',
            name='birthdate',
            field=models.DateField(null=True, verbose_name=b'Geburtstag', blank=True),
        ),
    ]
