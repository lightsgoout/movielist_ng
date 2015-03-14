# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='omdb_id',
            field=models.IntegerField(unique=True, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='movie',
            name='rating_tomatoes',
            field=models.PositiveSmallIntegerField(blank=True, null=True, db_index=True, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)]),
            preserve_default=True,
        ),
    ]
