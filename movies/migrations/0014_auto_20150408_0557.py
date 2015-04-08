# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0013_usertomovie_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='slug',
            field=models.SlugField(blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='person',
            name='slug',
            field=models.SlugField(blank=True),
            preserve_default=True,
        ),
    ]
