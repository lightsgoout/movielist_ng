import datetime
from django.core import validators
from django.db import models
from django.db.models import QuerySet
from django.utils import translation
from django.utils.text import slugify
from model_utils.managers import PassThroughManager
from common import fields


class MovieQuerySet(QuerySet):
    def without_image(self):
        return self.filter(
            image_imdb=''
        )

    def with_image(self):
        return self.exclude(image_imdb='')

    def without_translation(self):
        return self.filter(
            title_ru=''
        )

    def with_translation(self):
        return self.exclude(title_ru='')


class TopManager(models.Manager):
    def imdb(self):
        return self.get_queryset().filter(
            votes_imdb__isnull=False,
            rating_imdb__isnull=False,
        ).extra(
            select={'imdb_points': 'votes_imdb * rating_imdb'},
            order_by=['-imdb_points']
        )


class Movie(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    OMDB = 0
    IMDB = 1
    KINOPOISK = 2

    SOURCES = (
        (OMDB, 'OMDB'),
        (IMDB, 'IMDB'),
        (KINOPOISK, 'KINOPOISK'),
    )
    source = models.PositiveSmallIntegerField(choices=SOURCES, default=0)
    source_last_updated_at = models.DateTimeField(null=True, blank=True)

    title_en = models.CharField(max_length=255, blank=True)
    title_ru = models.CharField(max_length=255, blank=True)
    year = models.PositiveSmallIntegerField(null=True, db_index=True)
    date_released = models.DateField(null=True, blank=True, db_index=True)
    slug = models.SlugField(blank=True)

    imdb_processed = models.BooleanField(default=False, db_index=True)

    kinopoisk_id = models.IntegerField(unique=True, null=True, blank=True)
    imdb_id = models.CharField(max_length=16, unique=True, null=True)
    omdb_id = models.IntegerField(unique=True, null=True, blank=True)

    directors = models.ManyToManyField('movies.Person', related_name='directed_movies', blank=True)
    writers = models.ManyToManyField('movies.Person', related_name='written_movies', blank=True, through='movies.WriterToMovie')
    cast = models.ManyToManyField('movies.Person', related_name='starred_movies', blank=True, through='movies.ActorToMovie')
    producers = models.ManyToManyField('movies.Person', related_name='produced_movies', blank=True)
    composers = models.ManyToManyField('movies.Person', related_name='composed_movies', blank=True)
    genres = models.ManyToManyField('movies.Genre', related_name='movies', blank=True)
    countries = models.ManyToManyField('common.Country', related_name='movies', blank=True)

    # runtime in minutes
    runtime = models.PositiveSmallIntegerField(
        null=True,
        blank=True
    )
    tagline = models.CharField(max_length=255, blank=True)

    plot_en = models.TextField(max_length=1500, blank=True)
    plot_ru = models.TextField(max_length=1500, blank=True)
    full_plot_en = models.TextField(max_length=8000, blank=True)
    full_plot_ru = models.TextField(max_length=8000, blank=True)

    rating_kinopoisk = models.DecimalField(
        max_digits=5,
        decimal_places=3,
        null=True,
        blank=True,
        db_index=True)
    rating_imdb = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        null=True,
        blank=True,
        db_index=True)
    rating_metacritic = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        db_index=True,
        validators=[
            validators.MaxValueValidator(100),
            validators.MinValueValidator(0),
        ])
    rating_tomatoes = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        db_index=True,
        validators=[
            validators.MaxValueValidator(100),
            validators.MinValueValidator(0),
        ])
    tomatoes_fresh = models.NullBooleanField(blank=True)

    image_imdb = models.URLField(blank=True, max_length=512)

    rated = fields.MovieRatedField(blank=True, db_index=True)

    votes_imdb = models.PositiveIntegerField(null=True, blank=True, db_index=True)
    votes_kinopoisk = models.PositiveIntegerField(null=True, blank=True, db_index=True)

    objects = PassThroughManager.for_queryset_class(MovieQuerySet)()
    top = TopManager()

    def __unicode__(self):
        if self.title_ru:
            return u'{} ({}) - {}'.format(self.title_en, self.year, self.title_ru)
        return u'{} ({})'.format(self.title_en, self.year)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title_en)
        return super(Movie, self).save(*args, **kwargs)

    @property
    def title(self):
        cur_language = translation.get_language()
        if cur_language == 'ru':
            return self.title_ru or self.title_en
        else:
            return self.title_en or self.title_ru

    @property
    def plot(self):
        cur_language = translation.get_language()
        if cur_language == 'ru':
            return self.plot_ru
        else:
            return self.plot_en

    @property
    def full_plot(self):
        cur_language = translation.get_language()
        if cur_language == 'ru':
            return self.full_plot_ru
        else:
            return self.full_plot_en

    @property
    def image_url(self):
        if self.image_imdb:
            return self.image_imdb
        elif self.kinopoisk_id:
            return u'http://st.kp.yandex.net/images/film_iphone/iphone360_{}.jpg'.format(self.kinopoisk_id)

    @property
    def imdb_url(self):
        if self.imdb_id:
            return u'www.imdb.com/title/{}/'.format(self.imdb_id)
        return None

    @property
    def kinopoisk_url(self):
        if self.kinopoisk_id:
            return u'www.kinopoisk.ru/film/{}/'.format(self.kinopoisk_id)
        return None

    @property
    def unique_writers(self):
        return self.writers.all().distinct()

    """
    This methods use manual slicing to make use of prefetch_related.
    """
    def get_top_cast(self):
        cast = list(self.cast.all())
        return cast[:15]

    def get_short_cast(self):
        cast = list(self.cast.all())
        return cast[:4]

    def get_series_information(self):
        series = self.chains.filter(is_direct_series=True)
        if len(series) > 0:
            series = series[0]
            movies = series.movies.all().order_by('year')
            next_movie = None
            prev_movie = None
            for index, movie in enumerate(movies):
                if self == movie:
                    if index > 0:
                        prev_movie = movies[index-1]
                    try:
                        next_movie = movies[index+1]
                    except IndexError:
                        pass
                    break

            return series, next_movie, prev_movie
        return None, None, None

    class Meta:
        app_label = 'movies'
