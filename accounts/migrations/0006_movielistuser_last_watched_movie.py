# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0009_auto_20150328_0103'),
        ('accounts', '0005_auto_20150331_0018'),
    ]

    operations = [
        migrations.AddField(
            model_name='movielistuser',
            name='last_watched_movie',
            field=models.ForeignKey(related_name='users_last_watched', blank=True, to='movies.Movie', null=True),
            preserve_default=True,
        ),
    ]
