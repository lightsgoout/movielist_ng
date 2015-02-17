# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('common', '0001_initial'),
        ('achievements', '0001_initial'),
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movielistuser',
            name='achievements',
            field=models.ManyToManyField(to='achievements.Achievement', through='achievements.UserToAchievement', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='movielistuser',
            name='country',
            field=models.ForeignKey(blank=True, to='common.Country', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='movielistuser',
            name='friends',
            field=models.ManyToManyField(related_name='friends_rel_+', to=settings.AUTH_USER_MODEL, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='movielistuser',
            name='movies',
            field=models.ManyToManyField(to='movies.Movie', through='movies.UserToMovie', blank=True),
            preserve_default=True,
        ),
    ]
