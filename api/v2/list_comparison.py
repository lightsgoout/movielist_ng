from django.conf.urls import url
from tastypie import fields
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.exceptions import NotFound
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash
from accounts.models import MovielistUser
from api.v2.movie_short import MovieShortResource
from movies.models import UserToMovie


class ListComparisonResource(ModelResource):
    movie = fields.ToOneField(
        MovieShortResource,
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
        queryset = UserToMovie.objects.all().select_related('movie').order_by('-id')
        resource_name = 'list_comparison'
        authentication = Authentication()
        authorization = Authorization()
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        include_resource_uri = False
        limit = 25
        filtering = {
            'status': ('exact',),
        }

        fields = [
            'score',
            'status',
        ]

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/shared_with%s$" % (
                self._meta.resource_name,
                trailing_slash()),
                self.wrap_view('shared_with'),
                name="api_shared_list"),
        ]

    def shared_with(self, request, **kwargs):
        self.method_check(request, allowed=['get'])

        try:
            user1 = MovielistUser.objects.get(username=request.GET.get('first_username'))
        except MovielistUser.DoesNotExist:
            raise NotFound('User does not exist')

        try:
            user2 = MovielistUser.objects.get(username=request.GET.get('second_username'))
        except MovielistUser.DoesNotExist:
            raise NotFound('User does not exist')

        movies = user1.get_shared_movies(user2,
                                         from_queryset=self._meta.queryset)

        bundles = []
        for obj in movies:
            bundle = self.build_bundle(obj=obj, request=request)
            dehydrated = self.full_dehydrate(bundle, for_list=True)
            bundles.append(dehydrated)

        return self.create_response(request, bundles)

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
