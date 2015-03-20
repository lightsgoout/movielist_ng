# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0005_movie_imdb_processed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='imdb_processed',
            field=models.BooleanField(default=False, db_index=True),
            preserve_default=True,
        ),
    ]
