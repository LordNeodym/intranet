# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filer.fields.image


class Migration(migrations.Migration):

    dependencies = [
        ('filer', '0002_auto_20150606_2003'),
        ('core', '0016_auto_20150909_2247'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=50, verbose_name=b'Kategorie')),
            ],
            options={
                'verbose_name': 'Bilderkategorie',
                'verbose_name_plural': 'Bilderkategorien',
            },
        ),
        migrations.CreateModel(
            name='SingleImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.ForeignKey(related_name='image_imagecategory', to='core.ImageCategory')),
                ('image', filer.fields.image.FilerImageField(related_name='image', verbose_name=b'Image', to='filer.Image')),
            ],
            options={
                'verbose_name': 'Bild',
                'verbose_name_plural': 'Bilder',
            },
        ),
    ]
