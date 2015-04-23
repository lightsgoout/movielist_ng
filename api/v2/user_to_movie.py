from django.db.models import Q
from tastypie import fields
from tastypie.authentication import Authentication
from tastypie.exceptions import BadRequest, NotFound
from tastypie.resources import ModelResource
from accounts.models import MovielistUser
from api.v2.movie import MovieResource
from movies.models import UserToMovie


class UserToMovieResource(ModelResource):
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
        fields = [
            'created_at',
            'score',
            'status',
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

    def dehydrate_my_score(self, bundle):
        if bundle.request.user.is_authenticated():
            """
            obj.my_score is populated at self.obj_get_list.
            """
            my_score = getattr(bundle.obj, 'my_score', None)
            if my_score:
                return int(my_score)
        return None

    def dehydrate_score(self, bundle):
        if bundle.obj.score:
            return int(bundle.obj.score)
        return bundle.obj.score

    def dehydrate_my_status(self, bundle):
        if bundle.request.user.is_authenticated():
            """
            obj.my_status is populated at self.obj_get_list.
            """
            if hasattr(bundle.obj, 'my_status'):
                return bundle.obj.my_status
        return None
