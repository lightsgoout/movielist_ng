# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movies', '0009_auto_20150328_0103'),
        ('achievements', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('event_type', models.SmallIntegerField(choices=[(0, b'User watched movie'), (1, b'User planned to watch movie'), (2, b'User followed another user'), (3, b'Achievement unlocked'), (4, b'Achievement locked'), (5, b'User scored movie')])),
                ('arg_achievement', models.ForeignKey(blank=True, to='achievements.Achievement', null=True)),
                ('arg_movie', models.ForeignKey(blank=True, to='movies.Movie', null=True)),
                ('arg_user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('user', models.ForeignKey(related_name='events', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
