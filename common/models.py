from django.db import models


class Country(models.Model):
    name_en = models.CharField(max_length=256, unique=True)
    name_ru = models.CharField(max_length=256, blank=True)

    class Meta:
        ordering = (
            'name_en',
        )

    def __unicode__(self):
        return self.name_en

