from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
import re
from accounts.models import MovielistUser
from common.feature_framework import feature_enabled
from movies import constants
from movies.models import Movie, Person, MovieChain
from settings import features


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
        ).order_by('id')[:constants.COMPATIBILITY_SHARED_MOVIES_COUNT]
        total_shared_counter = len(shared_movies)

        if request.user != user:
            following = request.user.is_following(user)
        else:
            following = None
    else:
        compatibility_power, shared_movies = -1, []
        total_shared_counter = 0
        following = None

    status_counters = user.get_status_counters()
    total_watched = status_counters.get(constants.WATCHED, 0)
    total_plan_to_watch = status_counters.get(constants.PLAN_TO_WATCH, 0)
    total_ignored = status_counters.get(constants.IGNORED, 0)
    total_achievements = user.get_achievements().count()

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
            'total_watched': total_watched,
            'total_plan_to_watch': total_plan_to_watch,
            'total_ignored': total_ignored,
            'total_achievements': total_achievements,
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
        ).order_by('id')[:constants.COMPATIBILITY_SHARED_MOVIES_COUNT]
        total_shared_counter = len(shared_movies)

        if request.user != user:
            following = request.user.is_following(user)
        else:
            following = None
    else:
        compatibility_power, shared_movies = -1, []
        total_shared_counter = 0
        following = None

    status_counters = user.get_status_counters()
    total_watched = status_counters.get(constants.WATCHED, 0)
    total_plan_to_watch = status_counters.get(constants.PLAN_TO_WATCH, 0)
    total_ignored = status_counters.get(constants.IGNORED, 0)
    total_achievements = user.get_achievements().count()

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
            'total_watched': total_watched,
            'total_plan_to_watch': total_plan_to_watch,
            'total_ignored': total_ignored,
            'total_achievements': total_achievements,
        }
    )


def show_movie(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    series, next_movie, prev_movie = movie.get_series_information()
    return render(
        request,
        'pages/movie/movie.html',
        {
            'movie': movie,
            'cast': movie.get_top_cast(),
            'series': series,
            'next_movie': next_movie,
            'prev_movie': prev_movie,
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


def search(request):
    query = request.GET.get('q')
    if not query:
        return redirect('/')

    query = query.strip()

    if len(query) < 3:
        return render(
            request,
            'pages/search/search_results.html',
            {
                'movies': [],
                'people': [],
                'query': query,
            }
        )

    """
    If query ends with a digit e.g `Saw 3` try to find matching movie in a
    movie chain. In this case it will be Saw III
    """
    if re.search(r' \d$', query):
        base_part = query[:-1].strip()
        chains = MovieChain.objects.filter(
            Q(movies__title_en__icontains=base_part) |
            Q(movies__title_ru__icontains=base_part)
        ).distinct()
        if len(chains) == 1:
            """
            We found an exact match, for example "iron_man" series for a
            Iron Man 3 query.
            Now we should take N'th movie from a serie.
            """
            n = int(query[-1]) - 1  # 0-based indexing
            try:
                movie = chains[0].movies.all().order_by('year')[n]
                return redirect('movie', movie.id)
            except IndexError:
                """
                When this approach doesn't work fall back to default logic.
                """
                pass

    """
    Movie lookup.
    """
    if feature_enabled(features.SPHINX_SEARCH):
        movies = Movie.search.query(query).order_by('-rating_imdb')
    else:
        movies = Movie.objects.prefetch_related(
            'genres',
            'countries',
            'directors',
            'cast',
            'composers',
        ).filter(
            Q(title_en__icontains=query) |
            Q(title_ru__icontains=query)
        ).order_by('-rating_imdb')

    """
    Person lookup.
    """
    if feature_enabled(features.SPHINX_SEARCH):
        people = Person.search.query(query).order_by('-sort_power')
    else:
        people = Person.objects.filter(
            Q(name_en__icontains=query) |
            Q(name_ru__icontains=query)
        ).order_by('-sort_power')

    """
    If only one movie found and no people then
    redirect straight to the movie page.
    """
    if len(movies) == 1 and len(people) == 0:
        return redirect('movie', movies[0].id)

    """
    Same for people.
    """
    if len(movies) == 0 and len(people) == 1:
        return redirect('person', people[0].id)

    return render(
        request,
        'pages/search/search_results.html',
        {
            'movies': movies,
            'people': people,
            'query': query,
        }
    )
