from django.db import models
from movies import constants


class UserToMovie(models.Model):
    SCORE_CHOICES = (
        ('1.0', '1.0'),
        ('1.5', '1.5'),
        ('2.0', '2.0'),
        ('2.5', '2.5'),
        ('3.0', '3.0'),
        ('3.5', '3.5'),
        ('4.0', '4.0'),
        ('4.5', '4.5'),
        ('5.0', '5.0'),
        ('5.5', '5.5'),
        ('6.0', '6.0'),
        ('6.5', '6.5'),
        ('7.0', '7.0'),
        ('7.5', '7.5'),
        ('8.0', '8.0'),
        ('8.5', '8.5'),
        ('9.0', '9.0'),
        ('9.5', '9.5'),
        ('10.0', '10.0'),
    )

    user = models.ForeignKey('accounts.MovielistUser')
    movie = models.ForeignKey('movies.Movie')
    score = models.DecimalField(
        decimal_places=1,
        max_digits=3,
        choices=SCORE_CHOICES,
        null=True,
        blank=True,
        db_index=True,
    )
    status = models.CharField(
        choices=constants.STATUS_CHOICES,
        max_length=1,
        default=constants.WATCHED,
        db_index=True)

    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        app_label = 'movies'
        unique_together = (
            ('user', 'movie'),
        )


class WriterRole(models.Model):
    name_en = models.CharField(max_length=255, unique=True)
    name_ru = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return self.name_en

    class Meta:
        app_label = 'movies'


class WriterToMovie(models.Model):
    person = models.ForeignKey('movies.Person')
    movie = models.ForeignKey('movies.Movie')
    role = models.ForeignKey(WriterRole, null=True, blank=True)

    class Meta:
        app_label = 'movies'
        unique_together = (
            ('person', 'movie', 'role')
        )


class ActorToMovie(models.Model):
    person = models.ForeignKey('movies.Person')
    movie = models.ForeignKey('movies.Movie')
    character_en = models.CharField(max_length=64, blank=True)
    character_ru = models.CharField(max_length=64, blank=True)

    class Meta:
        app_label = 'movies'
        unique_together = (
            ('person', 'movie', 'character_en')
        )
