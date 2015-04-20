from django.db import models


class ImportListJob(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey('accounts.MovielistUser')
    kinopoisk_id = models.CharField(blank=True, max_length=16)
    finished = models.BooleanField(default=False, db_index=True)
    progress = models.PositiveSmallIntegerField(default=0)
