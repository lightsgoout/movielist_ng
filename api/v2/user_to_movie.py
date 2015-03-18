import json
from django.conf.urls import url
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

    class Meta:
        queryset = UserToMovie.objects.all().\
            select_related('movie').\
            prefetch_related(
                'movie__genres',
                'movie__countries',
                'movie__directors',
                'movie__cast',
            ).order_by('-id')
        resource_name = 'user_to_movie'
        authentication = Authentication()
        authorization = UserObjectsOnlyAuthorization()
        list_allowed_methods = ['get']
        detail_allowed_methods = ['put', 'get']
        limit = 25
        filtering = {
            'status': ('exact',),
        }

    def build_filters(self, filters=None):
        username = filters.get('username')
        if not username:
            raise BadRequest('Username filter is required')

        try:
            user = MovielistUser.objects.get(username=username)
        except MovielistUser.DoesNotExist:
            raise NotFound('User does not exist')

        built_filters = super(UserToMovieResource, self).build_filters(filters)
        built_filters['user'] = user
        return built_filters

    def dehydrate_score(self, bundle):
        if bundle.obj.score:
            return float(bundle.obj.score)
        return bundle.obj.score

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/add_movie%s$" % (
                self._meta.resource_name,
                trailing_slash()),
                self.wrap_view('add_movie'),
                name="api_add_movie"),
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

        request.user.add_movie(movie, status)

        result = {
            'ok': True,
        }

        return self.create_response(request, result)

