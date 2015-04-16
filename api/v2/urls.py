from django.conf.urls import patterns, url, include
from api.v2.genre import GenreResource
from api.v2.list_comparison import ListComparisonResource
from api.v2.movie import MovieResource
from api.v2.movie_short import MovieShortResource
from api.v2.user import UserResource
from api.v2.user_to_movie import UserToMovieResource


user_to_movie = UserToMovieResource()
list_comparison = ListComparisonResource()
genres = GenreResource()
movies = MovieResource()
movies_short = MovieShortResource()
users = UserResource()

urlpatterns = patterns(
    '',
    url(r'', include(user_to_movie.urls)),
    url(r'', include(genres.urls)),
    url(r'', include(movies.urls)),
    url(r'', include(movies_short.urls)),
    url(r'', include(users.urls)),
    url(r'', include(list_comparison.urls)),
)
