from django.db import models
from django.db.models import Sum, QuerySet
from model_utils.managers import PassThroughManager


class PersonQuerySet(QuerySet):
    def without_translation(self):
        return self.filter(
            name_ru=''
        )

    def with_translation(self):
        return self.exclude(name_ru='')


class Person(models.Model):
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

    def get_starred_movies(self):
        return self.starred_movies.all().order_by('-year')

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

    class Meta:
        app_label = 'movies'
        ordering = ['-sort_power']
