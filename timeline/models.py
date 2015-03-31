from django.db import models
from django.dispatch import receiver
from common import feature_framework
from settings import features
from timeline import constants as timeline_constants
from movies import signals as movie_signals, constants
from accounts import signals as account_signals
from achievements import signals as achievement_signals


class Event(models.Model):

    user = models.ForeignKey('accounts.MovielistUser', related_name='events')
    timestamp = models.DateTimeField(auto_now_add=True)

    event_type = models.SmallIntegerField(
        choices=timeline_constants.EVENT_TYPE_CHOICES,
    )

    arg_movie = models.ForeignKey('movies.Movie', null=True, blank=True)
    arg_user = models.ForeignKey('accounts.MovielistUser', null=True, blank=True)
    arg_achievement = models.ForeignKey('achievements.Achievement', null=True, blank=True)
    arg_score = models.DecimalField(
        decimal_places=1,
        max_digits=3,
        null=True,
        blank=True,
    )


# noinspection PyUnusedLocal
@receiver(movie_signals.user_added_movie)
@feature_framework.is_enabled(features.TIMELINE)
def timeline_user_added_movie(user, movie, status, score, **kwargs):
    """
    @type user accounts.models.MovielistUser
    @type movie movies.models.Movie
    @type score decimal.Decimal or None
    """
    """
    Transaction is opened at UserMixin* APIs
    """
    if status == constants.WATCHED:
        Event.objects.create(
            user=user,
            arg_movie=movie,
            event_type=timeline_constants.USER_WATCHED_MOVIE,
        )
    elif status == constants.PLAN_TO_WATCH:
        Event.objects.create(
            user=user,
            arg_movie=movie,
            event_type=timeline_constants.USER_PLAN_TO_WATCH_MOVIE,
        )


# noinspection PyUnusedLocal
@receiver(movie_signals.user_scored_movie)
@feature_framework.is_enabled(features.TIMELINE)
def timeline_user_scored_movie(user, movie, score, **kwargs):
    """
    @type user accounts.models.MovielistUser
    @type movie movies.models.Movie
    @type score decimal.Decimal or None
    """
    """
    Transaction is opened at UserMixin* APIs
    """
    Event.objects.create(
        user=user,
        arg_movie=movie,
        arg_score=score,
        event_type=timeline_constants.USER_SCORED_MOVIE,
    )


# noinspection PyUnusedLocal
@receiver(account_signals.user_followed)
@feature_framework.is_enabled(features.TIMELINE)
def timeline_user_followed(user, friend, **kwargs):
    """
    @type user accounts.models.MovielistUser
    @type friend accounts.models.MovielistUser
    """
    """
    Transaction is opened at UserMixin* APIs
    """
    Event.objects.create(
        user=user,
        arg_user=friend,
        event_type=timeline_constants.USER_FOLLOWED,
    )
    Event.objects.create(
        user=friend,
        arg_user=user,
        event_type=timeline_constants.USER_FOLLOWING,
    )


# noinspection PyUnusedLocal
@receiver(achievement_signals.achievement_unlocked)
@feature_framework.is_enabled(features.TIMELINE)
def timeline_achievement_unlocked(user, achievement, **kwargs):
    """
    @type user accounts.models.MovielistUser
    @type achievement achievements.models.Achievement
    """
    """
    Transaction is opened at UserMixin* APIs
    """
    Event.objects.create(
        user=user,
        arg_achievement=achievement,
        event_type=timeline_constants.ACHIEVEMENT_UNLOCKED,
    )


# noinspection PyUnusedLocal
@receiver(achievement_signals.achievement_locked)
@feature_framework.is_enabled(features.TIMELINE)
def timeline_achievement_locked(user, achievement, **kwargs):
    """
    @type user accounts.models.MovielistUser
    @type achievement achievements.models.Achievement
    """
    """
    Transaction is opened at UserMixin* APIs
    """
    Event.objects.create(
        user=user,
        arg_achievement=achievement,
        event_type=timeline_constants.ACHIEVEMENT_LOCKED,
    )
