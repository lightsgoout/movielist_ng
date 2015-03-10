from tastypie import fields
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.exceptions import BadRequest, NotFound
from tastypie.resources import ModelResource
from accounts.models import MovielistUser
from api.v2.movie import MovieResource
from movies.models import UserToMovie


class UserToMovieResource(ModelResource):

    movie = fields.ToOneField(MovieResource, 'movie', full=True, null=True)

    class Meta:
        queryset = UserToMovie.objects.all().select_related('movie').order_by('-id')
        resource_name = 'user_to_movie'
        authentication = Authentication()
        authorization = Authorization()
        list_allowed_methods = ['get']
        limit = 50
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

    # def dehydrate(self, bundle):
    #     bundle.data['score'] = "2.5"
    #     return bundle
