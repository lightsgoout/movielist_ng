import datetime
from django.db import models
from django.db.models import Q
from django.dispatch import receiver
from common import fields, feature_framework
from movies import constants, signals
from settings import features


class Achievement(models.Model):

    code = models.CharField(max_length=8, unique=True)
    title_en = models.CharField(max_length=64)
    title_ru = models.CharField(max_length=64, blank=True)
    description_en = models.TextField(max_length=255)
    description_ru = models.TextField(max_length=255, blank=True)

    added_on = models.DateField(auto_now_add=True)

    is_enabled = models.BooleanField(default=True, db_index=True)
    is_hidden = models.BooleanField(default=False, db_index=True)
    is_manual = models.BooleanField(default=False, db_index=True)

    # Achievement conditions
    condition_deadline = models.DateField(null=True, blank=True, db_index=True)
    condition_movie = models.ForeignKey('movies.Movie', null=True, blank=True)
    condition_movie_year = models.PositiveSmallIntegerField(null=True,  blank=True, db_index=True)
    condition_movie_rated = fields.MovieRatedField(null=True, blank=True, db_index=True)
    condition_movie_imdb_rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        null=True,
        blank=True,
    )
    condition_movie_country = models.ForeignKey('common.Country', null=True, blank=True)
    condition_movie_genre = models.ForeignKey('movies.Genre', null=True, blank=True)
    condition_movie_person = models.ForeignKey('movies.Person', null=True, blank=True)
    condition_chain = models.ForeignKey('movies.MovieChain', null=True, blank=True)
    condition_rate_movie_more_than = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        null=True,
        blank=True,
    )
    condition_rate_movie_less_than = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        null=True,
        blank=True,
    )

    condition_total_runtime_more_than = models.PositiveIntegerField(
        null=True,
        blank=True,
    )
    condition_total_watched_more_than = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    condition_times = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        app_label = 'achievements'


def is_achievement_satisfied(achievement, user, just_added_movie):
    """
    @type achievement Achievement
    @type user accounts.models.MovielistUser
    @type just_added_movie movies.models.Movie
    """
    if achievement.condition_deadline:
        if datetime.date.today() > achievement.condition_deadline:
            return False

    if achievement.condition_movie:
        if just_added_movie != achievement.condition_movie:
            return False

    if achievement.condition_total_runtime_more_than:
        total_runtime = user.get_total_movie_runtime(constants.WATCHED)
        if total_runtime <= achievement.condition_total_runtime_more_than:
            return False

    if achievement.condition_total_watched_more_than:
        total_watched = user.get_movies(constants.WATCHED).count()
        if total_watched <= achievement.condition_total_watched_more_than:
            return False

    if achievement.condition_movie_year:
        if just_added_movie.year != achievement.condition_movie_year:
            return False

        if achievement.condition_times:
            if user.get_movies(
                constants.WATCHED,
                year=achievement.condition_movie_year,
            ).count() != achievement.condition_times:
                return False

    if achievement.condition_movie_rated:
        if just_added_movie.rated != achievement.condition_movie_rated:
            return False

        if achievement.condition_times:
            if user.get_movies(
                constants.WATCHED,
                rated=achievement.condition_movie_rated,
            ).count() != achievement.condition_times:
                return False

    return True


@receiver(signals.user_watched_movie)
@feature_framework.is_enabled(features.ACHIEVEMENTS)
def unlock_achievements(user, movie, score, **kwargs):
    """
    @type user accounts.models.MovielistUser
    @type movie movies.models.Movie
    @type score decimal.Decimal or None
    """
    # Collect achievements which are about certain movie conditions
    # (year, MPAA rating, etc.)
    movie_achievements = Achievement.objects.filter(
        Q(condition_movie=movie) |
        Q(condition_movie_year=movie.year) |
        Q(condition_movie_rated=movie.rated)
    ).exclude(
        users=user,
    )

    for movie_achievement in movie_achievements:
        if is_achievement_satisfied(movie_achievement, user, movie):
            user.add_achievement(movie_achievement)


# noinspection PyUnusedLocal
@receiver(signals.user_removed_movie)
@feature_framework.is_enabled(features.ACHIEVEMENTS)
def lock_achievements(user, movie, score, **kwargs):
    """
    @type user accounts.models.MovielistUser
    @type movie movies.models.Movie
    @type score decimal.Decimal or None
    """
    user.get_achievements(
        condition_movie=movie
    ).delete()
