from datetime import date
from django.db import models
from django.db.models import Sum, QuerySet
import itertools
from model_utils.managers import PassThroughManager


class PersonQuerySet(QuerySet):
    def without_translation(self):
        return self.filter(
            name_ru=''
        )

    def with_translation(self):
        return self.exclude(name_ru='')


class Person(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    name_en = models.CharField(max_length=255, unique=True)
    name_ru = models.CharField(max_length=255, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    birth_year = models.PositiveSmallIntegerField(null=True, blank=True)
    kinopoisk_id = models.IntegerField(null=True, blank=True, db_index=True)
    imdb_id = models.CharField(max_length=16, blank=True, db_index=True)

    sort_power = models.FloatField(
        null=True,
        blank=True,
        default=0,
        db_index=True
    )

    objects = PassThroughManager.for_queryset_class(PersonQuerySet)()

    def __unicode__(self):
        return self.name_en

    @property
    def name(self):
        from django.utils import translation
        cur_language = translation.get_language()
        if cur_language == 'ru':
            return self.name_ru or self.name_en
        else:
            return self.name_en

    @property
    def image_url(self):
        if self.kinopoisk_id:
            return u'http://st.kp.yandex.net/images/actor_iphone/iphone360_{}.jpg'.format(self.kinopoisk_id)
        return None

    def get_top_movies(self):
        # Make use of prefetch_related
        starred_movies = [
            (m.id, m.title, m.rating_imdb) for m in self.starred_movies.all()]
        directed_movies = [
            (m.id, m.title, m.rating_imdb) for m in self.directed_movies.all()]
        written_movies = [
            (m.id, m.title, m.rating_imdb) for m in self.written_movies.all()]
        composed_movies = [
            (m.id, m.title, m.rating_imdb) for m in self.composed_movies.all()]
        produced_movies = [
            (m.id, m.title, m.rating_imdb) for m in self.produced_movies.all()]

        # Do manual sorting to avoid N queries for N people
        full_list = list(itertools.chain(
            starred_movies,
            directed_movies,
            written_movies,
            composed_movies,
            produced_movies
        ))

        # Sort by '-rating_imdb'
        full_list.sort(key=lambda tup: tup[2], reverse=True)
        return full_list[:4]

    def update_sort_power(self):
        total_starred_rating = self.starred_movies.all().\
            aggregate(Sum('rating_imdb'))['rating_imdb__sum']

        total_movies = self.starred_movies.all().count()
        if total_starred_rating and total_movies:
            self.sort_power = (
                round(total_starred_rating / total_movies, 2) +
                1 * (total_movies - 1)
            )
            self.save(update_fields=('sort_power',))

    @property
    def age(self):
        today = date.today()
        if self.birth_date:
            born = self.birth_date
        elif self.birth_year:
            born = date(self.birth_year, 1, 1)
        else:
            return None
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    class Meta:
        app_label = 'movies'
        ordering = ['-sort_power']
