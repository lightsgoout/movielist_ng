from django.conf.urls import patterns, url
from movies.models import UserToMovie

urlpatterns = patterns(
    '',
    url(r'^list/(?P<username>[\w.@+-]+)/watched/$',
        'movies.views.show_list',
        {'status': UserToMovie.WATCHED},
        name='list_watched'),
    url(r'^list/(?P<username>[\w.@+-]+)/plantowatch/$',
        'movies.views.show_list',
        {'status': UserToMovie.PLAN_TO_WATCH},
        name='list_plantowatch'),
    url(r'^list/(?P<username>[\w.@+-]+)/ignored/$',
        'movies.views.show_list',
        {'status': UserToMovie.IGNORED},
        name='list_ignored'),
    url(r'^movie/(?P<movie_id>[\d]+)/$',
        'movies.views.show_movie',
        name='movie'),
)
