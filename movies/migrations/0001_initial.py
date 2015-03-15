# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import common.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ActorToMovie',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('character_en', models.CharField(max_length=64, blank=True)),
                ('character_ru', models.CharField(max_length=64, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name_en', models.CharField(unique=True, max_length=64)),
                ('name_ru', models.CharField(max_length=64, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('source', models.PositiveSmallIntegerField(default=0, choices=[(0, b'OMDB'), (1, b'IMDB'), (2, b'KINOPOISK')])),
                ('source_last_updated_at', models.DateTimeField(null=True, blank=True)),
                ('title_en', models.CharField(max_length=255, blank=True)),
                ('title_ru', models.CharField(max_length=255, blank=True)),
                ('year', models.PositiveSmallIntegerField(null=True, db_index=True)),
                ('date_released', models.DateField(db_index=True, null=True, blank=True)),
                ('kinopoisk_id', models.IntegerField(unique=True, null=True, blank=True)),
                ('imdb_id', models.CharField(unique=True, max_length=16)),
                ('omdb_id', models.IntegerField(unique=True, null=True, blank=True)),
                ('runtime', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('tagline', models.CharField(max_length=255, blank=True)),
                ('plot_en', models.TextField(max_length=1500, blank=True)),
                ('plot_ru', models.TextField(max_length=1500, blank=True)),
                ('full_plot_en', models.TextField(max_length=8000, blank=True)),
                ('full_plot_ru', models.TextField(max_length=8000, blank=True)),
                ('rating_kinopoisk', models.DecimalField(db_index=True, null=True, max_digits=5, decimal_places=3, blank=True)),
                ('rating_imdb', models.DecimalField(db_index=True, null=True, max_digits=3, decimal_places=1, blank=True)),
                ('rating_metacritic', models.PositiveSmallIntegerField(blank=True, null=True, db_index=True, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)])),
                ('rating_tomatoes', models.PositiveSmallIntegerField(blank=True, null=True, db_index=True, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)])),
                ('tomatoes_fresh', models.NullBooleanField()),
                ('image_imdb', models.URLField(max_length=512, blank=True)),
                ('rated', common.fields.MovieRatedField(blank=True, max_length=5, db_index=True, choices=[(b'G', b'G'), (b'PG', b'PG'), (b'PG-13', b'PG-13'), (b'R', b'R'), (b'NC-17', b'NC-17')])),
                ('votes_imdb', models.PositiveIntegerField(db_index=True, null=True, blank=True)),
                ('votes_kinopoisk', models.PositiveIntegerField(db_index=True, null=True, blank=True)),
                ('is_trashed', models.BooleanField(default=False, db_index=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MovieChain',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('system_name', models.CharField(unique=True, max_length=32)),
                ('name_en', models.CharField(unique=True, max_length=255)),
                ('name_ru', models.CharField(max_length=255, blank=True)),
                ('is_direct_series', models.BooleanField(default=False)),
                ('movies', models.ManyToManyField(related_name='chains', to='movies.Movie')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name_en', models.CharField(unique=True, max_length=255)),
                ('name_ru', models.CharField(max_length=255, blank=True)),
                ('birth_date', models.DateField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserToMovie',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.DecimalField(blank=True, null=True, max_digits=3, decimal_places=1, choices=[(b'1.0', b'1.0'), (b'1.5', b'1.5'), (b'2.0', b'2.0'), (b'2.5', b'2.5'), (b'3.0', b'3.0'), (b'3.5', b'3.5'), (b'4.0', b'4.0'), (b'4.5', b'4.5'), (b'5.0', b'5.0'), (b'5.5', b'5.5'), (b'6.0', b'6.0'), (b'6.5', b'6.5'), (b'7.0', b'7.0'), (b'7.5', b'7.5'), (b'8.0', b'8.0'), (b'8.5', b'8.5'), (b'9.0', b'9.0'), (b'9.5', b'9.5'), (b'10.0', b'10.0')])),
                ('status', models.CharField(default=b'W', max_length=1, db_index=True, choices=[(b'W', b'Watched'), (b'P', b'Plan to watch'), (b'I', b'Ignored')])),
                ('movie', models.ForeignKey(to='movies.Movie')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WriterRole',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name_en', models.CharField(unique=True, max_length=255)),
                ('name_ru', models.CharField(max_length=255, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WriterToMovie',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('movie', models.ForeignKey(to='movies.Movie')),
                ('person', models.ForeignKey(to='movies.Person')),
                ('role', models.ForeignKey(blank=True, to='movies.WriterRole', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='writertomovie',
            unique_together=set([('person', 'movie', 'role')]),
        ),
        migrations.AlterUniqueTogether(
            name='usertomovie',
            unique_together=set([('user', 'movie')]),
        ),
        migrations.AddField(
            model_name='movie',
            name='cast',
            field=models.ManyToManyField(related_name='starred_movies', through='movies.ActorToMovie', to='movies.Person', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='movie',
            name='composers',
            field=models.ManyToManyField(related_name='composed_movies', to='movies.Person', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='movie',
            name='countries',
            field=models.ManyToManyField(related_name='movies', to='common.Country', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='movie',
            name='directors',
            field=models.ManyToManyField(related_name='directed_movies', to='movies.Person', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='movie',
            name='genres',
            field=models.ManyToManyField(related_name='movies', to='movies.Genre', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='movie',
            name='producers',
            field=models.ManyToManyField(related_name='produced_movies', to='movies.Person', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='movie',
            name='writers',
            field=models.ManyToManyField(related_name='written_movies', through='movies.WriterToMovie', to='movies.Person', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='actortomovie',
            name='movie',
            field=models.ForeignKey(to='movies.Movie'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='actortomovie',
            name='person',
            field=models.ForeignKey(to='movies.Person'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='actortomovie',
            unique_together=set([('person', 'movie', 'character_en')]),
        ),
    ]
