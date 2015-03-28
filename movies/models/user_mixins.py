from decimal import Decimal
from django.db import models
from movies import constants, signals
from .relations import UserToMovie


class UserMoviesMixin(models.Model):
    class Meta:
        abstract = True

    movies = models.ManyToManyField(
        'movies.Movie',
        through='movies.UserToMovie',
        blank=True,)

    def get_total_movie_runtime(self, status=constants.WATCHED):
        return self.movies.\
            filter(usertomovie__status=status).\
            aggregate(total_runtime=models.Sum('runtime'))['total_runtime']

    def get_total_movie_runtime_days(self, status=constants.WATCHED):
        total_runtime = self.get_total_movie_runtime(status)
        if not total_runtime:
            return 0
        return (Decimal(total_runtime)/60/24).quantize(Decimal('0.1'))

    def get_average_movie_score(self):
        avg_score = UserToMovie.objects.filter(
            user=self,
            status=constants.WATCHED
        ).aggregate(avg_score=models.Avg('score'))['avg_score']
        return round(avg_score, 1)

    def get_movies(self, status=constants.WATCHED, **kwargs):
        return self.movies.filter(usertomovie__status=status, **kwargs)

    def add_movie(self, movie, status=constants.WATCHED, score=None):
        """
        @type movie movies.models.Movie
        @type status str
        @type score decimal.Decimal
        """
        u2m = UserToMovie.objects.create(
            user=self,
            movie=movie,
            status=status,
            score=score,
        )
        signals.user_added_movie.send(
            sender=self.__class__,
            user=self,
            movie=movie,
            status=status,
            score=score)
        return u2m

    def remove_movie(self, movie):
        u2m = UserToMovie.objects.get(
            user=self,
            movie=movie
        )
        u2m.delete()
        signals.user_removed_movie.send(
            sender=self.__class__,
            user=self,
            movie=movie,
            status=u2m.status,
            score=u2m.score)
        return u2m

    def get_movie_status(self, movie):
        try:
            return UserToMovie.objects.get(
                user=self,
                movie=movie
            )
        except UserToMovie.DoesNotExist:
            return None

    def get_compatibility(self, user):
        """
        @type user accounts.models.MovielistUser
        """
        if user == self:
            return 100

        his_approved_movies = UserToMovie.objects.filter(
            user=user,
            status=constants.WATCHED,
            score__gte=constants.COMPATIBILITY_MOVIE_APPROVED_SCORE,
        ).values_list('movie', flat=True)
        if len(his_approved_movies) < constants.COMPATIBILITY_MINIMUM_MOVIES_REQUIRED:
            return -1

        my_approved_movies = UserToMovie.objects.filter(
            user=self,
            status=constants.WATCHED,
            score__gte=constants.COMPATIBILITY_MOVIE_APPROVED_SCORE,
        ).values_list('movie', flat=True)
        if len(my_approved_movies) < constants.COMPATIBILITY_MINIMUM_MOVIES_REQUIRED:
            return -1
        """
        100% compatibility is when all my_approved_movies contained within
        his_approved_movies
        """
        intersection = set(his_approved_movies) & set(my_approved_movies)
        return int(
            round(len(intersection) / float(len(his_approved_movies)) * 100)
        )
