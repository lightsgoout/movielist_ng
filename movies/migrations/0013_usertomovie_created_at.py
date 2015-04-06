# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0012_remove_movie_is_trashed'),
    ]

    operations = [
        migrations.AddField(
            model_name='usertomovie',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 4, 6, 22, 28, 49, 508186), auto_now_add=True),
            preserve_default=False,
        ),
    ]
