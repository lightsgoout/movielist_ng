import datetime
from django.db import models
from django.db.models import Q
from django.dispatch import receiver
from django.utils import translation
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

    @property
    def title(self):
        cur_language = translation.get_language()
        if cur_language == 'ru':
            return self.title_ru
        else:
            return self.title_en

    @property
    def description(self):
        cur_language = translation.get_language()
        if cur_language == 'ru':
            return self.description_ru
        else:
            return self.description_en

    class Meta:
        app_label = 'achievements'


def is_achievement_satisfied(achievement, user, movie, score):
    """
    @type achievement Achievement
    @type user accounts.models.MovielistUser
    @type movie movies.models.Movie
    @type score decimal.Decimal
    """
    if achievement.condition_deadline:
        if datetime.date.today() > achievement.condition_deadline:
            return False

    if achievement.condition_movie:
        if movie != achievement.condition_movie:
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
        if movie.year != achievement.condition_movie_year:
            return False

        if achievement.condition_times:
            if user.get_movies(
                constants.WATCHED,
                year=achievement.condition_movie_year,
            ).count() != achievement.condition_times:
                return False

    if achievement.condition_movie_rated:
        if movie.rated != achievement.condition_movie_rated:
            return False

        if achievement.condition_times:
            if user.get_movies(
                constants.WATCHED,
                rated=achievement.condition_movie_rated,
            ).count() != achievement.condition_times:
                return False

    if achievement.condition_rate_movie_less_than:
        if score >= achievement.condition_rate_movie_less_than:
            return False

    if achievement.condition_rate_movie_more_than:
        if score <= achievement.condition_rate_movie_more_than:
            return False

    return True


@receiver(signals.user_added_movie)
@feature_framework.is_enabled(features.ACHIEVEMENTS)
def unlock_movie_achievements(user, movie, status, score, **kwargs):
    """
    @type user accounts.models.MovielistUser
    @type movie movies.models.Movie
    @type score decimal.Decimal or None
    """
    if status != constants.WATCHED:
        return

    # Collect achievements which are about certain movie conditions
    # (year, MPAA rating, etc.)
    movie_achievements = Achievement.objects.filter(
        Q(condition_movie=movie) |
        Q(condition_movie_year=movie.year) |
        Q(condition_movie_rated=movie.rated)
    ).exclude(
        users=user,
    )
    """
    Transaction is opened at UserMixin* APIs
    """
    for movie_achievement in movie_achievements:
        if is_achievement_satisfied(movie_achievement, user, movie, score):
            user.add_achievement(movie_achievement)


# noinspection PyUnusedLocal
@receiver(signals.user_removed_movie)
@feature_framework.is_enabled(features.ACHIEVEMENTS)
def lock_movie_achievements(user, movie, status, score, **kwargs):
    """
    @type user accounts.models.MovielistUser
    @type movie movies.models.Movie
    @type score decimal.Decimal or None
    """
    """
    Transaction is opened at UserMixin* APIs
    """
    achievements = user.get_achievements(
        Q(condition_movie=movie)
    )
    for achievement in achievements:
        user.remove_achievement(achievement)


@receiver(signals.user_scored_movie)
@feature_framework.is_enabled(features.ACHIEVEMENTS)
def unlock_movie_score_achievements(user, movie, score, **kwargs):

    achievements = Achievement.objects.filter(
        Q(
            condition_movie=movie,
        ) &
        Q(
            Q(condition_rate_movie_more_than__lt=score) |
            Q(condition_rate_movie_less_than__gt=score)
        )
    ).exclude(
        users=user,
    )
    """
    Transaction is opened at UserMixin* APIs
    """
    for movie_achievement in achievements:
        if is_achievement_satisfied(movie_achievement, user, movie, score):
            user.add_achievement(movie_achievement)


@receiver(signals.user_changed_score)
@feature_framework.is_enabled(features.ACHIEVEMENTS)
def recheck_movie_score_achievements(user, movie, new_score, old_score, **kwargs):
    achievements = user.get_achievements(
        Q(condition_movie=movie)
    )
    for achievement in achievements:
        if not is_achievement_satisfied(achievement, user, movie, new_score):
            user.remove_achievement(achievement)
