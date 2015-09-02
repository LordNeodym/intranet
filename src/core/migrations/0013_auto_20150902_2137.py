# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20150902_0044'),
    ]

    operations = [
        migrations.RenameField(
            model_name='round',
            old_name='win',
            new_name='winner',
        ),
    ]
