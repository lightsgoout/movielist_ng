from django.db import models


class MovieChain(models.Model):
    name_en = models.CharField(max_length=255, unique=True)
    name_ru = models.CharField(max_length=255, blank=True)
    movies = models.ManyToManyField('movies.Movie', related_name='chains')

    def __unicode__(self):
        return self.name_en

    class Meta:
        app_label = 'movies'
