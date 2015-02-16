from django.core import validators
from django.db import models
from django.db.models import QuerySet
from django.utils import translation
from model_utils.managers import PassThroughManager


class MovieQuerySet(QuerySet):
    def without_image(self):
        return self.filter(
            image_imdb=''
        )

    def with_image(self):
        return self.exclude(image_imdb='')


class TopManager(models.Manager):
    def imdb(self):
        return self.get_queryset().filter(
            votes_imdb__isnull=False,
            rating_imdb__isnull=False,
        ).order_by(
            '-votes_imdb',
            '-rating_imdb',
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

    kinopoisk_id = models.IntegerField(unique=True, null=True, blank=True)
    imdb_id = models.CharField(max_length=16, unique=True)

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
        ]
    )

    image_imdb = models.URLField(blank=True, max_length=512)

    RATINGS = (
        ('G', 'G'),
        ('PG', 'PG'),
        ('PG-13', 'PG-13'),
        ('R', 'R'),
        ('NC-17', 'NC-17'),
    )
    rated = models.CharField(
        choices=RATINGS,
        max_length=5,
        blank=True,
        db_index=True,
    )

    votes_imdb = models.PositiveIntegerField(null=True, blank=True, db_index=True)
    votes_kinopoisk = models.PositiveIntegerField(null=True, blank=True, db_index=True)

    is_trashed = models.BooleanField(default=False, db_index=True)

    objects = PassThroughManager.for_queryset_class(MovieQuerySet)()
    top = TopManager()

    def __unicode__(self):
        if self.title_ru:
            return u'{} ({}) - {}'.format(self.title_en, self.year, self.title_ru)
        return u'{} ({})'.format(self.title_en, self.year)

    @property
    def title(self):
        cur_language = translation.get_language()
        if cur_language == 'ru':
            return self.title_ru
        else:
            return self.title_en

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
        return self.image_imdb

    class Meta:
        app_label = 'movies'
