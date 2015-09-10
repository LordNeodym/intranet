# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_imagecategory_singleimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagecategory',
            name='description',
            field=models.CharField(unique=True, max_length=50, verbose_name=b'Kategorie'),
        ),
        migrations.AlterField(
            model_name='videocategory',
            name='description',
            field=models.CharField(unique=True, max_length=50, verbose_name=b'Kategorie'),
        ),
    ]
