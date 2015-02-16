# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movielistuser',
            name='movies',
            field=models.ManyToManyField(to='movies.Movie', through='movies.UserToMovie', blank=True),
            preserve_default=True,
        ),
    ]
