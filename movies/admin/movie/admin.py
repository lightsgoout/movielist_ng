# coding=utf-8
from common.utils import admincolumn, SphinxModelAdmin
from movies.admin.movie import filters, actions


class MovieAdmin(SphinxModelAdmin):
    list_display = (
        'title_en',
        'title_ru',
        'year',
        'kinopoisk_id',
        'imdb_id',
        'rating_kinopoisk',
        'rating_imdb',
        'votes_kinopoisk',
        'votes_imdb',
        'rated',
        'movie_directors',
        'movie_cast',
    )
    list_filter = (
        'source',
        'countries',
        'rated',
        'genres',
        filters.ImageFilter,
        filters.TranslatedFilter,
    )
    search_fields = (
        '=id',
        '=imdb_id',
        '=kinopoisk_id',
        '=year',
        'title_en',
        'title_ru',
    )
    ordering = ('-votes_imdb',)
    exclude = (
        'cast',
        'producers',
        'composers',
        'writers',
        'directors',
    )

    list_editable = ('title_ru',)

    actions = [
        actions.kinopoisk_fetch_movie_info,
    ]

    @admincolumn(u'Режиссер')
    def movie_directors(self, obj):
        """
        @type obj movies.models.Movie
        """
        return u', '.join(obj.directors.all().values_list('name_en', flat=True))

    @admincolumn(u'Актеры')
    def movie_cast(self, obj):
        """
        @type obj movies.models.Movie
        """
        return u', '.join(obj.cast.all().values_list('name_en', flat=True))
