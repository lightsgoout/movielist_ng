from movies.models import Movie
from suggestions.base import AbstractSuggester


class IMDBSuggester(AbstractSuggester):

    def next_in_top(self, movie):
        """
        @type movie movies.models.Movie
        """
        try:
            return Movie.top.imdb().filter(
                rating_imdb__lte=movie.rating_imdb
            ).exclude(
                pk=movie.pk,
            )[0]
        except IndexError:
            return None
