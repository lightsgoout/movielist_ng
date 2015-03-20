# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0004_auto_20150318_0756'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='imdb_processed',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
