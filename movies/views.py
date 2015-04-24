from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
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
        return redirect(reverse('list_watched', args=[request.user.username]))
    else:
        return redirect(reverse('login'))


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
        total_shared_counter = Movie.objects.filter(pk__in=shared_movies).count()
        shared_movies = Movie.objects.filter(
            pk__in=shared_movies
        ).order_by('id')[:constants.COMPATIBILITY_SHARED_MOVIES_COUNT]

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
            'logged_in': 'true' if request.user.is_authenticated() else 'false',
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


def show_movie(request, movie_id, slug):
    movie = get_object_or_404(Movie, pk=movie_id, slug=slug)
    series, next_movie, prev_movie = movie.get_series_information()
    if request.user.is_authenticated():
        opinions = request.user.get_following_opinions_about_movie(movie)
    else:
        opinions = []
    return render(
        request,
        'pages/movie/movie.html',
        {
            'movie': movie,
            'cast': movie.get_top_cast(),
            'series': series,
            'next_movie': next_movie,
            'prev_movie': prev_movie,
            'opinions': opinions,
        }
    )


def show_person(request, person_id, slug):
    person = get_object_or_404(Person, pk=person_id, slug=slug)
    return render(
        request,
        'pages/person/person.html',
        {
            'person': person,
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


def compare_list(request, first_username, second_username, mode=constants.COMPARE_MODE_SHARED):
    first_user = get_object_or_404(MovielistUser, username=first_username)
    second_user = get_object_or_404(MovielistUser, username=second_username)

    return render(
        request,
        'pages/user/compare/compare.html',
        {
            'first_user': first_user,
            'second_user': second_user,
            'mode': mode,
            'constants': constants,
        }
    )


def search(request):
    query = request.GET.get('q')
    if not query:
        return redirect('/')

    query = query.strip().lower()

    if len(query) < settings.SEARCH_QUERY_MINIMUM_LENGTH:
        return render(
            request,
            'pages/search/serp.html',
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
        movies = Movie.search.query(
            query
        ).order_by('-rating_imdb')
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
        people = Person.search.query(
            query
        ).order_by('-sort_power')[:settings.SEARCH_RESULTS_PER_PAGE]
    else:
        people = Person.objects.filter(
            Q(name_en__icontains=query) |
            Q(name_ru__icontains=query)
        ).prefetch_related(
            'starred_movies',
            'produced_movies',
            'written_movies',
            'composed_movies',
            'directed_movies',
        ).order_by('-sort_power')[:settings.SEARCH_RESULTS_PER_PAGE]

    """
    If only one movie found and no people then
    redirect straight to the movie page.
    """
    if len(movies) == 1 and len(people) == 0:
        movie = movies[0]
        return redirect('movie', movie.id, movie.slug)

    """
    Same for people.
    """
    if len(movies) == 0 and len(people) == 1:
        person = people[0]
        return redirect('person', person.id, person.slug)

    """
    Get information about user's watched movies to prepare frontend.
    """
    if request.user.is_authenticated():
        watched_movies = set(request.user.\
            get_movies(status=constants.WATCHED).\
            values_list('id', flat=True))
        plan_to_watch_movies = set(request.user.\
            get_movies(status=constants.PLAN_TO_WATCH).\
            values_list('id', flat=True))
    else:
        watched_movies = {}
        plan_to_watch_movies = {}

    if movies:
        movies = movies[:settings.SEARCH_RESULT_PER_PAGE]

    if people:
        people = people[:settings.SEARCH_RESULT_PER_PAGE]

    return render(
        request,
        'pages/search/serp.html',
        {
            'movies': movies,
            'people': people,
            'query': query,
            'SEARCH_RESULTS_PER_PAGE': settings.SEARCH_RESULTS_PER_PAGE,
            'SEARCH_QUERY_MINIMUM_LENGTH': settings.SEARCH_QUERY_MINIMUM_LENGTH,
            'watched_movies': watched_movies,
            'plan_to_watch_movies': plan_to_watch_movies,
            'constants': constants,
        }
    )
