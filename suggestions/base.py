from django.db.models import Count


class AbstractSuggester(object):

    def __init__(self, user, shown_ids=()):
        """
        @type user accounts.models.MovielistUser
        @type shown_ids list
        """
        self.user = user
        self.exclude_ids = [m.pk for m in user.movies.all()]
        self.shown_ids = shown_ids

    def next_in_series(self, movie):
        """
        @type movie movies.models.Movie
        """
        chains = movie.chains.all().annotate(
            movie_count=Count('movies')
        ).order_by(
            'movie_count'
        )
        for chain in chains:
            all_exclude_ids = set(self.exclude_ids) | set(self.shown_ids)
            unlisted = chain.movies.all().exclude(
                pk__in=all_exclude_ids
            ).exclude(
                pk=movie.pk
            ).order_by(
                'year'
            )
            if len(unlisted) > 0:
                return unlisted[0]
            continue
        return None

    def next_in_top(self, movie):
        """
        @type movie movies.models.Movie
        """
        raise NotImplementedError
