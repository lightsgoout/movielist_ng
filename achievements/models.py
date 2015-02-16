from django.db import models


class Achievement(models.Model):

    code = models.CharField(max_length=8, unique=True)
    title_en = models.CharField(max_length=64)
    title_ru = models.CharField(max_length=64, blank=True)
    description_en = models.TextField(max_length=255)
    description_ru = models.TextField(max_length=255, blank=True)

    added_on = models.DateField(auto_now_add=True)

    is_enabled = models.BooleanField(default=True)
