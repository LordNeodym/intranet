# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20150831_2342'),
    ]

    operations = [
        migrations.AddField(
            model_name='round',
            name='win',
            field=models.ForeignKey(editable=False, to='core.Team', null=True),
        ),
        migrations.AlterField(
            model_name='round',
            name='pkt1',
            field=models.IntegerField(blank=True, null=True, verbose_name=b'Punkte Heim', validators=[core.validators.integer_only]),
        ),
        migrations.AlterField(
            model_name='round',
            name='pkt2',
            field=models.IntegerField(blank=True, null=True, verbose_name=b'Punkte Gast', validators=[core.validators.integer_only]),
        ),
    ]
