from tastypie import fields
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.exceptions import BadRequest, NotFound
from tastypie.resources import ModelResource
from accounts.models import MovielistUser
from api.v2.movie import MovieResource
from movies.models import UserToMovie


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
        list_allowed_methods = ['get', 'post']
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

    def hydrate(self, bundle):
        bundle = super(UserToMovieResource, self).hydrate(bundle)
        bundle.obj.user = bundle.request.user
        bundle.obj.movie_id = bundle.data['movie_id']
        return bundle
