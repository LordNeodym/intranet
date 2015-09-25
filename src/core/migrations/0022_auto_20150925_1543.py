# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0021_auto_20150915_2334'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserExtension',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('avatar', models.ImageField(upload_to=b'user_avatar', null=True, verbose_name=b'Avatar', blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Zus\xe4tzliche Angaben',
                'verbose_name_plural': 'Zus\xe4tzliche Angaben',
            },
        ),
        migrations.AlterModelOptions(
            name='team',
            options={'ordering': ['id'], 'verbose_name': 'Team', 'verbose_name_plural': 'Teams'},
        ),
        migrations.AlterField(
            model_name='match',
            name='player_per_team',
            field=models.IntegerField(verbose_name=b'Spieler pro Team', validators=[django.core.validators.MinValueValidator(b'1')]),
        ),
    ]
