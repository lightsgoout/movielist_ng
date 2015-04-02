from django.db import models


class Genre(models.Model):
    name_en = models.CharField(max_length=64, unique=True)
    name_ru = models.CharField(max_length=64, blank=True)

    def __unicode__(self):
        return self.name_en

    @property
    def name(self):
        from django.utils import translation
        cur_language = translation.get_language()
        if cur_language == 'ru':
            return self.name_ru
        else:
            return self.name_en

    class Meta:
        app_label = 'movies'
        ordering = ['name_en']
