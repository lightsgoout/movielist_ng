from django.db import models


class Country(models.Model):
    name_en = models.CharField(max_length=256, unique=True)
    name_ru = models.CharField(max_length=256, blank=True)

    iso_code = models.CharField(
        max_length=2,
        blank=True,
        null=True,
        unique=True
    )

    class Meta:
        ordering = (
            'name_en',
        )

    def __unicode__(self):
        return self.name

    @property
    def name(self):
        from django.utils import translation
        cur_language = translation.get_language()
        if cur_language == 'ru':
            return self.name_ru
        else:
            return self.name_en

