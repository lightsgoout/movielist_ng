from django.conf.urls import patterns, url, include
from api.v2.user_to_movie import UserToMovieResource


user_to_movie = UserToMovieResource()

urlpatterns = patterns(
    '',
    url(r'', include(user_to_movie.urls)),
)
