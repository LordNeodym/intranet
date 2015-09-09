# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filer.fields.file


class Migration(migrations.Migration):

    dependencies = [
        ('filer', '0002_auto_20150606_2003'),
        ('core', '0015_auto_20150906_2005'),
    ]

    operations = [
        migrations.CreateModel(
            name='SingleVideo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'verbose_name': 'Video',
                'verbose_name_plural': 'Videos',
            },
        ),
        migrations.CreateModel(
            name='VideoCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=50, verbose_name=b'Kategorie')),
            ],
            options={
                'verbose_name': 'Videokategorie',
                'verbose_name_plural': 'Videokategorien',
            },
        ),
        migrations.AddField(
            model_name='singlevideo',
            name='category',
            field=models.ForeignKey(related_name='video_videocategory', to='core.VideoCategory'),
        ),
        migrations.AddField(
            model_name='singlevideo',
            name='video',
            field=filer.fields.file.FilerFileField(related_name='video', verbose_name=b'Video', to='filer.File'),
        ),
    ]
