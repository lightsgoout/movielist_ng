from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from accounts.models import MovielistUser
from movies.models import Movie, UserToMovie


def runtime_in_days(movie_list):
    return sum([m.runtime for m in movie_list if m.runtime])/60/24


def index(request):
    if request.user.is_authenticated():
        return render(request, 'dashboard.html')
    else:
        return render(request, 'landing.html')


def show_list(request, username, status):
    user = get_object_or_404(MovielistUser, username=username)
    watched = user.movies.filter(usertomovie__status=status)

    if status == UserToMovie.WATCHED:
        template = 'list/watched.html'
    elif status == UserToMovie.PLAN_TO_WATCH:
        template = 'list/plan_to_watch.html'
    elif status == UserToMovie.IGNORED:
        template = 'list/ignored.html'
    else:
        raise Http404()

    return render(
        request,
        template,
        {
            'movies': watched,
            'days': runtime_in_days(watched),
            'user': user,
        },
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
