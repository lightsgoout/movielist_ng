from django.db import models
from django.db.models import Manager
from django.utils import translation


class SuggestableManager(models.Manager):

    def get_queryset(self):
        return super(SuggestableManager, self).get_queryset().filter(
            is_suggestable=True,
        )


class MovieChain(models.Model):
    system_name = models.CharField(max_length=32, unique=True)
    name_en = models.CharField(max_length=255, unique=True)
    name_ru = models.CharField(max_length=255, blank=True)
    movies = models.ManyToManyField('movies.Movie', related_name='chains')
    is_direct_series = models.BooleanField(default=False, db_index=True)
    is_suggestable = models.BooleanField(default=True, db_index=True)

    objects = Manager()
    suggestable = SuggestableManager()

    def __unicode__(self):
        return self.name_en

    @property
    def title(self):
        cur_language = translation.get_language()
        if cur_language == 'ru':
            return self.name_ru or self.name_en
        else:
            return self.name_en

    class Meta:
        app_label = 'movies'
