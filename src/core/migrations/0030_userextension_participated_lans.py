# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_auto_20161003_1549'),
    ]

    operations = [
        migrations.AddField(
            model_name='userextension',
            name='participated_lans',
            field=models.ManyToManyField(related_name='user_lan', verbose_name=b'Teilgenommene LANs', to='core.IntranetMeta', blank=True),
        ),
    ]
