import datetime
from django.db import models
from django.db.models import Sum
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from accounts.models import MovielistUser

from common import fields
from movies.models import Movie, UserToMovie


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


class UserToAchievement(models.Model):
    user = models.ForeignKey('accounts.MovielistUser')
    achievement = models.ForeignKey(Achievement)
    unlocked_on = models.DateField(
        auto_now_add=True
    )
    is_active = models.BooleanField(default=True, db_index=True)


def is_achievement_satisfied(achievement, user):
    """
    @type achievement Achievement
    @type user accounts.models.MovielistUser
    """
    if achievement.condition_deadline:
        if datetime.date.today() > achievement.condition_deadline:
            return False

    if achievement.condition_movie:
        if not user.movies.filter(usertomovie__status=UserToMovie.WATCHED).exists():
            return False

    if achievement.condition_total_runtime_more_than:
        total_runtime = user.movies.\
            filter(usertomovie__status=UserToMovie.WATCHED).\
            aggregate(total_runtime=Sum('runtime'))['total_runtime']
        if total_runtime <= achievement.condition_total_runtime_more_than:
            return False

    if achievement.condition_total_watched_more_than:
        total_watched = user.movies.filter(usertomovie__status=UserToMovie.WATCHED).count()
        if total_watched <= achievement.condition_total_watched_more_than:
            return False

    return True


@receiver(post_save, sender=UserToMovie, )
def process_achievements(instance, **kwargs):
    """
    @type instance movies.models.UserToMovie
    """
    # movies = Movie.objects.filter(pk__in=list(pk_set))

    movie_achievements = Achievement.objects.filter(
        condition_movie=instance.movie)

    for movie_achievement in movie_achievements:
        if is_achievement_satisfied(movie_achievement, instance.user):
            UserToAchievement.objects.get_or_create(
                user=instance.user,
                achievement=movie_achievement
            )




