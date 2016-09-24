# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_menuorder_singlemenuorder'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='singlemenuorder',
            options={'ordering': ['-order', '-name'], 'verbose_name': 'Einzel-Bestellung', 'verbose_name_plural': 'Einzel-Bestellungen'},
        ),
        migrations.AddField(
            model_name='menuorder',
            name='locked',
            field=models.BooleanField(default=False, verbose_name=b'Bestellung sperren?'),
        ),
        migrations.AddField(
            model_name='singlemenuorder',
            name='price',
            field=models.FloatField(blank=True, null=True, verbose_name=b'Preis', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(99.99)]),
        ),
    ]
