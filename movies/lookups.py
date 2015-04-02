from ajax_select import LookupChannel
from django.db.models import Q
from django.template import Context
from django.template.loader import get_template
from common.feature_framework import feature_enabled
from movies import models
from settings.features import SPHINX_SEARCH


class MovieLookup(LookupChannel):
    model = models.Movie

    def get_query(self, query, request):
        if feature_enabled(SPHINX_SEARCH):
            results = models.Movie.search.query(query)
        else:
            results = models.Movie.objects.filter(
                is_trashed=False,
            ).filter(
                Q(title_en__icontains=query) |
                Q(title_ru__icontains=query)
            )
        return results.order_by(
            '-votes_imdb',
            '-rating_imdb',
            '-year',
        )[:5]

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


class PersonLookup(LookupChannel):
    model = models.Person

    def get_query(self, q, request):
        if feature_enabled(SPHINX_SEARCH):
            results = models.Person.search.query(q)
        else:
            results = models.Person.objects.filter(
                Q(name_en__icontains=q) |
                Q(name_ru__icontains=q)
            )
        # return results.order_by(
        #     '-starred_movies__rating_imdb',
        # )[0:5]
        return results[:5]

    def get_result(self, obj):
        """
        @type obj movies.models.Person
        """
        return obj.name_en

    def format_match(self, obj):
        """
        @type obj movies.models.Person
        """
        return self.format_item_display(obj)

    def format_item_display(self, obj):
        """
        @type obj movies.models.Person
        """
        return u'{actor} ({top_movies})'.format(
            actor=obj.name_en,
            top_movies=u', '.join(
                obj.starred_movies.all().
                order_by('-rating_imdb').
                values_list('title_en', flat=True)[0:7]
            )
        )
