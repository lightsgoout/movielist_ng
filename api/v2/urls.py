from django.conf.urls import patterns, url, include
from api.v2.genre import GenreResource
from api.v2.user_to_movie import UserToMovieResource


user_to_movie = UserToMovieResource()
genres = GenreResource()

urlpatterns = patterns(
    '',
    url(r'', include(user_to_movie.urls)),
    url(r'', include(genres.urls)),
)
