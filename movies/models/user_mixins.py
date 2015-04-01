from decimal import Decimal
from django.db import models, transaction
from django.db.models import Count
from movies import constants, signals
from .relations import UserToMovie


class UserMoviesMixin(models.Model):
    class Meta:
        abstract = True

    movies = models.ManyToManyField(
        'movies.Movie',
        through='movies.UserToMovie',
        blank=True,)
    last_watched_movie = models.ForeignKey(
        'movies.Movie',
        null=True,
        blank=True,
        related_name='users_last_watched'
    )

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
        with transaction.atomic():
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
            if status == constants.WATCHED:
                self.last_watched_movie = movie
                self.save(update_fields=('last_watched_movie',))
        return u2m

    def set_movie_score(self, movie, score):
        """
        @type movie movies.models.Movie
        @type score decimal.Decimal
        """
        try:
            u2m = UserToMovie.objects.get(
                user=self,
                movie=movie
            )
            u2m.score = score
            with transaction.atomic():
                u2m.save(update_fields=('score',))
                signals.user_scored_movie.send(
                    sender=self.__class__,
                    user=self,
                    movie=movie,
                    score=u2m.score,
                )
        except UserToMovie.DoesNotExist:
            pass

    def remove_movie(self, movie):
        """
        @type movie movies.models.Movie
        """
        u2m = UserToMovie.objects.get(
            user=self,
            movie=movie
        )
        with transaction.atomic():
            u2m.delete()
            signals.user_removed_movie.send(
                sender=self.__class__,
                user=self,
                movie=movie,
                status=u2m.status,
                score=u2m.score)
        return u2m

    def get_movie_status(self, movie):
        """
        @type movie movies.models.Movie
        """
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

        @rtype: tuple(int, list[hotels.models.hotel.Hotel])
        """
        if user == self:
            return 100, []

        his_approved_movies = UserToMovie.objects.filter(
            user=user,
            status=constants.WATCHED,
            score__gte=constants.COMPATIBILITY_MOVIE_APPROVED_SCORE,
        ).values_list('movie', flat=True)
        if len(his_approved_movies) < constants.COMPATIBILITY_MINIMUM_MOVIES_REQUIRED:
            return -1, []

        my_approved_movies = UserToMovie.objects.filter(
            user=self,
            status=constants.WATCHED,
            score__gte=constants.COMPATIBILITY_MOVIE_APPROVED_SCORE,
        ).values_list('movie', flat=True)
        if len(my_approved_movies) < constants.COMPATIBILITY_MINIMUM_MOVIES_REQUIRED:
            return -1, []
        """
        100% compatibility is when all my_approved_movies contained within
        his_approved_movies
        """
        shared_movies = set(his_approved_movies) & set(my_approved_movies)

        compatibility_power = int(
            round(len(shared_movies) / float(len(his_approved_movies)) * 100)
        )

        return compatibility_power, shared_movies

    def get_status_counters(self):
        values = UserToMovie.objects.\
            filter(user=self).\
            values_list('status').\
            annotate(Count('status'))
        return dict(values)
