# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20150902_0025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='round',
            name='win',
            field=models.ForeignKey(related_name='round_win', editable=False, to='core.Team', null=True),
        ),
    ]
