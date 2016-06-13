# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0023_userextension_birthdate'),
    ]

    operations = [
        migrations.CreateModel(
            name='MenuOrder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(default=b'Pizzeria', max_length=255, verbose_name=b'Name')),
                ('timestamp', models.DateTimeField(verbose_name=b'Datum')),
                ('venue', models.CharField(max_length=255, null=True, verbose_name=b'Ort', blank=True)),
            ],
            options={
                'ordering': ['-timestamp'],
                'verbose_name': 'Bestellung',
                'verbose_name_plural': 'Bestellungen',
            },
        ),
        migrations.CreateModel(
            name='SingleMenuOrder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order_number', models.CharField(max_length=255, verbose_name=b'Bestellnummer')),
                ('extra', models.CharField(max_length=255, null=True, verbose_name=b'Extra', blank=True)),
                ('name', models.ForeignKey(verbose_name=b'Benutzer', to=settings.AUTH_USER_MODEL)),
                ('order', models.ForeignKey(verbose_name=b'Bestellung', to='core.MenuOrder')),
            ],
            options={
                'ordering': ['-order', 'name'],
                'verbose_name': 'Einzel-Bestellung',
                'verbose_name_plural': 'Einzel-Bestellungen',
            },
        ),
    ]
