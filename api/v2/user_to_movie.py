import json
from django.conf.urls import url
from django.db.models import Q
from django.http import Http404
from tastypie import fields
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.exceptions import BadRequest, NotFound
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash
from accounts.models import MovielistUser
from api.v2.movie import MovieResource
from movies import constants
from movies.models import UserToMovie, Movie


class UserObjectsOnlyAuthorization(Authorization):
    def update_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user


class UserToMovieResource(ModelResource):
    movie_id = fields.IntegerField()
    movie = fields.ToOneField(
        MovieResource,
        'movie',
        full=True,
        null=True,
        readonly=True,
    )
    my_score = fields.FloatField(
        null=True,
        readonly=True,
    )
    my_status = fields.CharField(
        null=True,
        readonly=True,
    )

    class Meta:
        queryset = UserToMovie.objects.all().\
            select_related('movie').\
            prefetch_related(
                'movie__genres',
                'movie__countries',
                'movie__directors',
                'movie__cast',
                'movie__composers',
            ).order_by('-created_at')
        resource_name = 'user_to_movie'
        authentication = Authentication()
        authorization = UserObjectsOnlyAuthorization()
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        include_resource_uri = False
        limit = 25
        filtering = {
            'status': ('exact',),
        }
        ordering = [
            'created_at',
            'score',
            'movie',
            'movie__rating_imdb',
            'movie__title',
        ]

    def build_filters(self, filters=None):
        username = filters.get('username')
        if not username:
            raise BadRequest('Username filter is required')

        status = filters.get('status')
        if not status:
            raise BadRequest('Status filter is required')

        try:
            user = MovielistUser.objects.get(username=username)
        except MovielistUser.DoesNotExist:
            raise NotFound('User does not exist')

        built_filters = super(UserToMovieResource, self).build_filters(filters)
        built_filters['user'] = user
        return built_filters

    def get_object_list(self, request):
        """
        Overriden for filtering purposes
        """
        object_list = super(UserToMovieResource, self).get_object_list(request)
        query = request.GET.get('query', None)
        if not query:
            return object_list

        return object_list.filter(
            Q(movie__title_en__icontains=query) |
            Q(movie__title_ru__icontains=query) |
            Q(movie__cast__name_en__icontains=query) |
            Q(movie__cast__name_ru__icontains=query) |
            Q(movie__directors__name_en__icontains=query) |
            Q(movie__directors__name_ru__icontains=query)
        ).distinct()

    def obj_get_list(self, bundle, **kwargs):
        objects = super(UserToMovieResource, self).obj_get_list(bundle, **kwargs)
        """
        Now populate request.user scores.
        We do it here to avoid N-count queries in dehydrate.
        """
        if bundle.request.user.is_authenticated():
            if bundle.request.user.username != bundle.request.GET.get('username'):
                shared_movies = UserToMovie.objects.filter(
                    user=bundle.request.user,
                    movie_id__in=objects.values_list('movie_id', flat=True),
                ).values_list('movie_id', 'score', 'status')
                score_map = dict()
                for movie_id, score, status in shared_movies:
                    score_map[movie_id] = (score, status)
                for obj in objects:
                    score, status = score_map.get(obj.movie.id, (None, None))
                    setattr(obj, 'my_score', score)
                    setattr(obj, 'my_status', status)

        return objects

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/add_movie%s$" % (
                self._meta.resource_name,
                trailing_slash()),
                self.wrap_view('add_movie'),
                name="api_add_movie"),
            url(r"^(?P<resource_name>%s)/remove_movie%s$" % (
                self._meta.resource_name,
                trailing_slash()),
                self.wrap_view('remove_movie'),
                name="api_remove_movie"),
            url(r"^(?P<resource_name>%s)/movie_status%s$" % (
                self._meta.resource_name,
                trailing_slash()),
                self.wrap_view('movie_status'),
                name="api_movie_status"),
            url(r"^(?P<resource_name>%s)/set_score%s$" % (
                self._meta.resource_name,
                trailing_slash()),
                self.wrap_view('set_score'),
                name="api_movie_set_score"),
        ]

    def add_movie(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        self.is_authenticated(request)

        try:
            raw_json = json.loads(request.body)
        except ValueError:
            raise BadRequest('Invalid json')

        try:
            movie = Movie.objects.get(pk=raw_json.get('movie_id'))
        except Movie.DoesNotExist:
            raise Http404('Movie does not exist')

        status = raw_json.get('status')
        if status not in {constants.IGNORED, constants.PLAN_TO_WATCH, constants.WATCHED}:
            raise BadRequest('Invalid status')

        u2m = request.user.add_movie(movie, status)

        result = {
            'id': u2m.id,
        }

        return self.create_response(request, result)

    def remove_movie(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        self.is_authenticated(request)

        try:
            raw_json = json.loads(request.body)
        except ValueError:
            raise BadRequest('Invalid json')

        try:
            movie = Movie.objects.get(pk=raw_json.get('movie_id'))
        except Movie.DoesNotExist:
            raise Http404('Movie does not exist')

        request.user.remove_movie(movie)

        result = {
            'ok': True,
        }

        return self.create_response(request, result)

    def set_score(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        self.is_authenticated(request)

        try:
            raw_json = json.loads(request.body)
        except ValueError:
            raise BadRequest('Invalid json')

        score = raw_json.get('score')
        if not 0 < score <= 10:
            raise BadRequest('Invalid score')

        try:
            movie = Movie.objects.get(pk=raw_json.get('movie_id'))
        except Movie.DoesNotExist:
            raise BadRequest('Movie does not exist')

        request.user.set_movie_score(movie, score)

        result = {
            'ok': True,
        }

        return self.create_response(request, result)

    def movie_status(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)

        movie_id = request.GET.get('movie_id')
        if not movie_id:
            raise BadRequest('Invalid movie_id')

        try:
            movie = Movie.objects.get(pk=movie_id)
        except Movie.DoesNotExist:
            raise Http404('Movie does not exist')

        u2m = request.user.get_movie_status(movie)

        if u2m:
            result = {
                'status': u2m.status,
                'score': u2m.score,
                'id': u2m.id,
            }
        else:
            result = None

        return self.create_response(request, result)

    def hydrate(self, bundle):
        bundle = super(UserToMovieResource, self).hydrate(bundle)
        if bundle.data['status'] != constants.WATCHED:
            bundle.data['score'] = None

        bundle.data['user'] = bundle.request.user
        return bundle

    def dehydrate_my_score(self, bundle):
        if bundle.request.user.is_authenticated():
            """
            obj.my_score is populated at self.obj_get_list.
            """
            my_score = getattr(bundle.obj, 'my_score', None)
            if my_score:
                return float(my_score)
        return None

    def dehydrate_score(self, bundle):
        if bundle.obj.score:
            return float(bundle.obj.score)
        return bundle.obj.score

    def dehydrate_my_status(self, bundle):
        if bundle.request.user.is_authenticated():
            """
            obj.my_status is populated at self.obj_get_list.
            """
            if hasattr(bundle.obj, 'my_status'):
                return bundle.obj.my_status
        return None
