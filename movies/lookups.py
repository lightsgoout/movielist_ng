from ajax_select import LookupChannel
from django.db.models import Q
from django.template import Context
from django.template.loader import get_template
from common.feature_framework import feature_enabled
from movies.models import Movie
from settings.features import SPHINX_SEARCH


class MovieLookup(LookupChannel):

    model = Movie

    def get_query(self, query, request):
        if feature_enabled(SPHINX_SEARCH):
            results = Movie.search.query(query)
        else:
            results = Movie.objects.filter(
                Q(title_en__icontains=query) |
                Q(title_ru__icontains=query)
            )
        return results.order_by(
            '-votes_imdb',
            '-rating_imdb',
            '-year',
        )[0:5]

    def get_result(self, obj):
        """
        @type obj movies.models.Movie
        """
        return obj.title_en

    def format_match(self, obj):
        """
        @type obj movies.models.Movie
        """
        return self.format_item_display(obj)

    def format_item_display(self, obj):
        """
        @type obj movies.models.Movie
        """
        return get_template('lookups/movie.html').render(Context({
            'movie': obj
        }))
