from django.conf.urls import patterns, url, include
from api.v2.user_movielist import UserMovieListResource


user_movielist = UserMovieListResource()

urlpatterns = patterns(
    '',
    url(r'', include(user_movielist.urls)),
)
