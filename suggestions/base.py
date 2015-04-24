from movies import constants
from movies.models import Movie, MovieChain
from suggestions import factors


class AbstractSuggester(object):

    def next_in_top(self, movie):
        """
        @type movie movies.models.Movie
        """
        raise NotImplementedError

    def get_suggestion_list(self, user, limit=25):
        """
        @type user accounts.models.MovielistUser
        """
        exclude_ids = set([m.pk for m in user.movies.all()])
        result = []

        # "Same series" suggestion. E.g All other Harry Potter movies when
        # watched Sorcerer's Stone
        # TODO: test that ignored movie series do not get suggested
        related_chain_ids = set(user.movies.filter(
            usertomovie__status__in=[constants.WATCHED, constants.PLAN_TO_WATCH],
            chains__isnull=False,
            chains__is_suggestable=True
        ).values_list('chains', flat=True))

        related_series = MovieChain.suggestable.\
            filter(id__in=related_chain_ids, is_direct_series=True).\
            prefetch_related('movies')
        for chain in related_series:
            chain_movies = sorted(chain.movies.all(), key=lambda m: m.year)
            for movie in chain_movies:
                if movie.id in exclude_ids:
                    continue
                result.append((movie, factors.FACTOR_SAME_SERIES))
                exclude_ids.add(movie.id)

        if len(result) > limit:
            return result[:limit]

        # Top IMDB suggestions
        top_imdb_movies = Movie.top.imdb().exclude(pk__in=list(exclude_ids))[:50]
        for movie in top_imdb_movies:
            result.append((movie, factors.FACTOR_IMDB_TOP))
            exclude_ids.add(movie.id)

        if len(result) > limit:
            return result[:limit]

        # TODO: calculate personal charts by actor, genre, etc.

        return result
