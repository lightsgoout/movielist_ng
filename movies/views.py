from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from accounts.models import MovielistUser
from movies import constants
from movies.models import Movie


def index(request):
    if request.user.is_authenticated():
        return render(request, 'dashboard.html')
    else:
        return render(request, 'landing.html')


def show_list(request, username, status):
    user = get_object_or_404(MovielistUser, username=username)

    # TODO: usertomovie relation should not be exposed
    movies = user.get_movies(status).order_by('-usertomovie__id')

    total_runtime = user.get_total_movie_runtime(status) or 0

    return render(
        request,
        'list/list_ng.html',
        {
            'movies': movies,
            'days': (Decimal(total_runtime)/60/24).quantize(Decimal('0.1')),
            'user': user,
            'status': status,
            'constants': constants,
        },
    )


def list_user_achievements(request, username, is_locked):
    user = get_object_or_404(MovielistUser, username=username)
    achievements = user.get_achievements(is_locked=is_locked)

    return render(
        request,
        'list/list.html',
        {
            'achievements': achievements,
            'user': user,
            'constants': constants,
        }
    )


def show_movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    return render(
        request,
        'pages/movie.html',
        {
            'movie': movie,
        }
    )



M_IMDB_TOP = 'imdb'
M_KINOPOISK = 'kp'
M_TOP_FRANCHISES = 'topfr'
M_TOP_MOVIES_BY_GENRE = 'topbygenre'
M_TOP_MOVIES_BY_ACTOR = 'topbyactor'


@login_required
def wizard(request, mode=M_IMDB_TOP):
    """
    @type request django.http.request.HttpRequest
    """
    watched = request.user.movies.all()

    if mode == M_IMDB_TOP:
        movies = Movie.top.imdb()
    elif mode == M_KINOPOISK:
        movies = Movie.top.kinopoisk()
    else:
        raise Http404()

    try:
        movie = movies.exclude(pk__in=[w.pk for w in watched])[0]
    except IndexError:
        # TODO: remember to handle this at frontend
        raise Http404()

    return render(
        request,
        'wizard/list.html',
        {
            'movie': movie,
        }
    )
