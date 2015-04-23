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
    score_left = fields.FloatField(
        null=True,
        readonly=True,
    )
    score_right = fields.FloatField(
        null=True,
        readonly=True,
    )

    class Meta:
        queryset = UserToMovie.objects.all().\
            select_related('movie').\
            order_by('-id')
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

        fields = []

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/shared_with%s$" % (
                self._meta.resource_name,
                trailing_slash()),
                self.wrap_view('shared_with'),
                name="api_shared_list"),
            url(r"^(?P<resource_name>%s)/unique_left%s$" % (
                self._meta.resource_name,
                trailing_slash()),
                self.wrap_view('unique_left'),
                name="api_shared_unique_left"),
            url(r"^(?P<resource_name>%s)/unique_right%s$" % (
                self._meta.resource_name,
                trailing_slash()),
                self.wrap_view('unique_right'),
                name="api_shared_unique_right"),
            url(r"^(?P<resource_name>%s)/stats%s$" % (
                self._meta.resource_name,
                trailing_slash()),
                self.wrap_view('stats'),
                name="api_user_stats"),
            url(r"^(?P<resource_name>%s)/stats_comparison%s$" % (
                self._meta.resource_name,
                trailing_slash()),
                self.wrap_view('stats_comparison'),
                name="api_user_stats_comparison"),
        ]

    def shared_with(self, request, **kwargs):
        self.method_check(request, allowed=['get'])

        try:
            user1 = MovielistUser.objects.get(
                username=request.GET.get('first_username'))
        except MovielistUser.DoesNotExist:
            raise NotFound('User does not exist')

        try:
            user2 = MovielistUser.objects.get(
                username=request.GET.get('second_username'))
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

    def unique_left(self, request, **kwargs):
        self.method_check(request, allowed=['get'])

        try:
            user1 = MovielistUser.objects.get(
                username=request.GET.get('first_username'))
        except MovielistUser.DoesNotExist:
            raise NotFound('User does not exist')

        try:
            user2 = MovielistUser.objects.get(
                username=request.GET.get('second_username'))
        except MovielistUser.DoesNotExist:
            raise NotFound('User does not exist')

        movies = user1.get_my_unique_movies(user2,
                                            from_queryset=self._meta.queryset)

        bundles = []
        for obj in movies:
            bundle = self.build_bundle(obj=obj, request=request)
            dehydrated = self.full_dehydrate(bundle, for_list=True)
            bundles.append(dehydrated)

        return self.create_response(request, bundles)

    def unique_right(self, request, **kwargs):
        self.method_check(request, allowed=['get'])

        try:
            user1 = MovielistUser.objects.get(
                username=request.GET.get('first_username'))
        except MovielistUser.DoesNotExist:
            raise NotFound('User does not exist')

        try:
            user2 = MovielistUser.objects.get(
                username=request.GET.get('second_username'))
        except MovielistUser.DoesNotExist:
            raise NotFound('User does not exist')

        movies = user1.get_his_unique_movies(user2,
                                             from_queryset=self._meta.queryset)

        bundles = []
        for obj in movies:
            bundle = self.build_bundle(obj=obj, request=request)
            dehydrated = self.full_dehydrate(bundle, for_list=True)
            bundles.append(dehydrated)

        return self.create_response(request, bundles)

    def stats(self, request, **kwargs):
        self.method_check(request, allowed=['get'])

        try:
            user = MovielistUser.objects.get(username=request.GET.get('username'))
        except MovielistUser.DoesNotExist:
            raise NotFound('User does not exist')

        result = user.get_score_counters()

        return self.create_response(request, result)

    def stats_comparison(self, request, **kwargs):
        self.method_check(request, allowed=['get'])

        try:
            first_user = MovielistUser.objects.get(username=request.GET.get('first_username'))
        except MovielistUser.DoesNotExist:
            raise NotFound('User does not exist')

        try:
            second_user = MovielistUser.objects.get(username=request.GET.get('second_username'))
        except MovielistUser.DoesNotExist:
            raise NotFound('User does not exist')

        first_user_stats = first_user.get_score_counters()
        second_user_stats = second_user.get_score_counters()

        result = {
            first_user.username: first_user_stats,
            second_user.username: second_user_stats,
        }

        return self.create_response(request, result)

    def dehydrate_score_left(self, bundle):
        if bundle.obj.score_left:
            return int(bundle.obj.score_left)
        return bundle.obj.score_left

    def dehydrate_score_right(self, bundle):
        if bundle.obj.score_right:
            return int(bundle.obj.score_right)
        return bundle.obj.score_right
