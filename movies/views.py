from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from accounts.models import MovielistUser
from movies import constants
from movies.models import Movie, Person


def index(request):
    if request.user.is_authenticated():
        return render(request, 'pages/dashboard/dashboard.html')
    else:
        return render(request, 'pages/landing/landing.html')


def show_followers(request, username):
    user = get_object_or_404(MovielistUser, username=username)
    return render(
        request,
        'pages/user/followers/followers.html',
        {
            'user': user,
            'following': user.get_following(),
            'followers': user.get_followers(),
        }
    )


def show_list(request, username, status):
    user = get_object_or_404(MovielistUser, username=username)
    if request.user.is_authenticated():
        compatibility_power, shared_movies = request.user.get_compatibility(user)
        shared_movies = Movie.objects.filter(pk__in=shared_movies)
        shared_movies = Movie.objects.filter(
            pk__in=shared_movies
        )[:constants.COMPATIBILITY_SHARED_MOVIES_COUNT]
        total_shared_counter = len(shared_movies)

        if request.user != user:
            following = request.user.is_following(user)
        else:
            following = None
    else:
        compatibility_power, shared_movies = -1, []
        total_shared_counter = 0
        following = None

    return render(
        request,
        'pages/user/list/list_ng.html',
        {
            'user': user,
            'status': status,
            'constants': constants,
            'compatibility_power': compatibility_power,
            'shared_movies': shared_movies,
            'shared_movies_remainder': (
                total_shared_counter - constants.COMPATIBILITY_SHARED_MOVIES_COUNT
            ),
            'editable': 'true' if request.user == user else 'false',
            'following': 'true' if following else 'false',
        },
    )


def list_user_achievements(request, username):
    user = get_object_or_404(MovielistUser, username=username)
    achievements = user.get_achievements()
    if request.user.is_authenticated():
        compatibility_power, shared_movies = request.user.get_compatibility(user)
        shared_movies = Movie.objects.filter(pk__in=shared_movies)
        shared_movies = Movie.objects.filter(
            pk__in=shared_movies
        )[:constants.COMPATIBILITY_SHARED_MOVIES_COUNT]
        total_shared_counter = len(shared_movies)

        if request.user != user:
            following = request.user.is_following(user)
        else:
            following = None
    else:
        compatibility_power, shared_movies = -1, []
        total_shared_counter = 0
        following = None

    return render(
        request,
        'pages/user/list/achievements.html',
        {
            'achievements': achievements,
            'user': user,
            'constants': constants,
            'compatibility_power': compatibility_power,
            'shared_movies': shared_movies,
            'shared_movies_remainder': (
                total_shared_counter - constants.COMPATIBILITY_SHARED_MOVIES_COUNT
            ),
            'editable': 'true' if request.user == user else 'false',
            'following': 'true' if following else 'false',
        }
    )


def show_movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    return render(
        request,
        'pages/movie/movie.html',
        {
            'movie': movie,
            'cast': movie.get_top_cast(),
        }
    )


def show_person(request, person_id):
    person = get_object_or_404(Person, pk=person_id)
    return render(
        request,
        'pages/person/person.html',
        {
            'person': person,
            'starred_movies': person.get_starred_movies(),
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
        'pages/wizard/wizard.html',
        {
            'movie': movie,
        }
    )


def compare_list(request, first_username, second_username):
    raise NotImplementedError
