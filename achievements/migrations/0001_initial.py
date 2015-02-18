# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import common.fields


# noinspection PyPep8
class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Achievement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(unique=True, max_length=8)),
                ('title_en', models.CharField(max_length=64)),
                ('title_ru', models.CharField(max_length=64, blank=True)),
                ('description_en', models.TextField(max_length=255)),
                ('description_ru', models.TextField(max_length=255, blank=True)),
                ('added_on', models.DateField(auto_now_add=True)),
                ('is_enabled', models.BooleanField(default=True, db_index=True)),
                ('is_hidden', models.BooleanField(default=False, db_index=True)),
                ('is_manual', models.BooleanField(default=False, db_index=True)),
                ('condition_deadline', models.DateField(db_index=True, null=True, blank=True)),
                ('condition_movie_year', models.PositiveSmallIntegerField(db_index=True, null=True, blank=True)),
                ('condition_movie_rated', common.fields.MovieRatedField(blank=True, max_length=5, null=True, db_index=True, choices=[(b'G', b'G'), (b'PG', b'PG'), (b'PG-13', b'PG-13'), (b'R', b'R'), (b'NC-17', b'NC-17')])),
                ('condition_movie_imdb_rating', models.DecimalField(null=True, max_digits=3, decimal_places=1, blank=True)),
                ('condition_rate_movie_more_than', models.DecimalField(null=True, max_digits=3, decimal_places=1, blank=True)),
                ('condition_rate_movie_less_than', models.DecimalField(null=True, max_digits=3, decimal_places=1, blank=True)),
                ('condition_total_runtime_more_than', models.PositiveIntegerField(null=True, blank=True)),
                ('condition_total_watched_more_than', models.PositiveIntegerField(null=True, blank=True)),
                ('condition_times', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('condition_chain', models.ForeignKey(blank=True, to='movies.MovieChain', null=True)),
                ('condition_movie', models.ForeignKey(blank=True, to='movies.Movie', null=True)),
                ('condition_movie_country', models.ForeignKey(blank=True, to='common.Country', null=True)),
                ('condition_movie_genre', models.ForeignKey(blank=True, to='movies.Genre', null=True)),
                ('condition_movie_person', models.ForeignKey(blank=True, to='movies.Person', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserToAchievement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('unlocked_on', models.DateField(auto_now_add=True)),
                ('is_locked', models.BooleanField(default=False, db_index=True)),
                ('achievement', models.ForeignKey(to='achievements.Achievement')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
