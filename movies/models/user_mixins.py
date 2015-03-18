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

    def is_movie_added(self, movie, status=constants.WATCHED):
        """
        @type movie movies.models.Movie
        @type status str
        """
        return self.movies.filter(
            usertomovie__movie=movie,
            usertomovie__status=status
        ).exists()
