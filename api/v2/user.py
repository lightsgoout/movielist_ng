import json
from django.conf.urls import url
from django.http import Http404
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.exceptions import BadRequest, NotFound
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash
from accounts.models import MovielistUser


class UserResource(ModelResource):
    class Meta:
        queryset = MovielistUser.objects.all()
        resource_name = 'user'
        authentication = Authentication()
        authorization = Authorization()
        list_allowed_methods = ['get']
        detail_allowed_methods = []
        include_resource_uri = False
        limit = 25
        fields = [
            'date_joined',
            'date_of_birth',
            'gender',
            'username',
        ]

    def build_filters(self, filters=None):
        username = filters.get('username')
        if not username:
            raise BadRequest('Username filter is required')

        try:
            """
            TODO: should work as-is, without filters.pop()
            (see UserToMovieResource.build_filters)
            """
            filters.pop('username', None)
            user = MovielistUser.objects.get(username=username)
        except MovielistUser.DoesNotExist:
            raise NotFound('User does not exist')

        built_filters = super(UserResource, self).build_filters(filters)
        built_filters['friends'] = user
        return built_filters

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/follow%s$" % (
                self._meta.resource_name,
                trailing_slash()),
                self.wrap_view('follow_user'),
                name="api_follow_user"),
            url(r"^(?P<resource_name>%s)/unfollow%s$" % (
                self._meta.resource_name,
                trailing_slash()),
                self.wrap_view('unfollow_user'),
                name="api_unfollow_user"),
            url(r"^(?P<resource_name>%s)/stats%s$" % (
                self._meta.resource_name,
                trailing_slash()),
                self.wrap_view('stats'),
                name="api_user_stats"),
        ]

    def follow_user(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        self.is_authenticated(request)

        try:
            raw_json = json.loads(request.body)
        except ValueError:
            raise BadRequest('Invalid json')

        try:
            user = MovielistUser.objects.get(username=raw_json.get('username'))
        except MovielistUser.DoesNotExist:
            raise Http404('User does not exist')

        request.user.follow_user(user)

        result = {
            'ok': True,
        }

        return self.create_response(request, result)

    def unfollow_user(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        self.is_authenticated(request)

        try:
            raw_json = json.loads(request.body)
        except ValueError:
            raise BadRequest('Invalid json')

        try:
            user = MovielistUser.objects.get(username=raw_json.get('username'))
        except MovielistUser.DoesNotExist:
            raise Http404('User does not exist')

        request.user.unfollow_user(user)

        result = {
            'ok': True,
        }

        return self.create_response(request, result)

    def stats(self, request, **kwargs):
        self.method_check(request, allowed=['get'])

        try:
            user = MovielistUser.objects.get(username=request.GET.get('username'))
        except MovielistUser.DoesNotExist:
            raise Http404('User does not exist')

        result = user.get_score_counters()

        return self.create_response(request, result)
