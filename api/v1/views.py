from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize, json
from django.db import IntegrityError
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import csrf_exempt
from movies.models import UserToMovie, Movie
import json as sjson
from suggestions.imdb import IMDBSuggester


class JsonResponse(HttpResponse):
    def __init__(self, data, status_code=200):
        if isinstance(data, QuerySet):
            content = serialize('json', data)
        else:
            content = sjson.dumps(
                data, indent=2, cls=json.DjangoJSONEncoder,
                ensure_ascii=False)
        super(JsonResponse, self).__init__(
            content, content_type='application/json', status=status_code)


class ApiOk(JsonResponse):
    def __init__(self, msg=None):
        super(ApiOk, self).__init__({
            'success': True,
            'msg': msg,
        })


class ApiFail(JsonResponse):
    def __init__(self, msg=None):
        super(ApiFail, self).__init__({
            'success': False,
            'msg': msg,
        }, status_code=503)


@csrf_exempt
@login_required
def add_to_list(request, movie_id, status=UserToMovie.WATCHED):
    """
    @type request django.http.request.HttpRequest
    @type movie_id int
    @type status str
    """
    try:
        UserToMovie.objects.get_or_create(
            movie_id=movie_id,
            user=request.user,
            status=status
        )
    except IntegrityError:
        return ApiFail(_(u'Movie does not exist'))

    return ApiOk(_(u'Movie added'))


@csrf_exempt
@login_required
def suggest_another_movie(request, movie_id, status=UserToMovie.WATCHED):
    """
    @type request django.http.request.HttpRequest
    @type movie_id int movie that was just added to list
    @type status str movie's status
    """
    movie = get_object_or_404(Movie, pk=movie_id)
    shown_ids = request.POST.get('shown_ids', '')
    if shown_ids:
        shown_ids = map(int, shown_ids.split(','))
    else:
        shown_ids = []
    suggester = IMDBSuggester(request.user, shown_ids=shown_ids)
    if status in {UserToMovie.WATCHED, UserToMovie.PLAN_TO_WATCH}:
        # User liked the movie or looking forward to it.
        # Suggest another from the series.
        choice = suggester.next_in_series(movie)
        if choice is None:
            choice = suggester.next_in_top(movie)
    else:
        choice = suggester.next_in_top(movie)

    if choice:
        return render(
            request,
            'wizard/movie.html',
            {
                'movie': choice,
            }
        )
    else:
        return ApiFail(_(u'No movies'))
