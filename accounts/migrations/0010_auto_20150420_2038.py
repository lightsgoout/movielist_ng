# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20150407_0123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movielistuser',
            name='last_watched_movie',
            field=models.ForeignKey(related_name='users_last_watched', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='movies.Movie', null=True),
            preserve_default=True,
        ),
    ]
