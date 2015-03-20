from django.db import models


class Person(models.Model):
    name_en = models.CharField(max_length=255, unique=True)
    name_ru = models.CharField(max_length=255, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    birth_year = models.PositiveSmallIntegerField(null=True, blank=True)
    kinopoisk_id = models.IntegerField(null=True, blank=True, db_index=True)
    imdb_id = models.CharField(max_length=16, blank=True, db_index=True)

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

    class Meta:
        app_label = 'movies'
