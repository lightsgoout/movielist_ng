import json
from django.conf.urls import url
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import Authorization
from tastypie.exceptions import BadRequest, NotFound
from tastypie.resources import Resource
from tastypie.utils import trailing_slash
from movies import constants
from movies.models import Movie


class MovieActionsResource(Resource):

    class Meta:
        resource_name = 'movie_actions'
        authentication = SessionAuthentication()
        authorization = Authorization()

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
            url(r"^(?P<resource_name>%s)/set_status%s$" % (
                self._meta.resource_name,
                trailing_slash()),
                self.wrap_view('set_status'),
                name="api_movie_set_status"),
            url(r"^(?P<resource_name>%s)/set_score%s$" % (
                self._meta.resource_name,
                trailing_slash()),
                self.wrap_view('set_score'),
                name="api_movie_set_score"),
            url(r"^(?P<resource_name>%s)/set_comments%s$" % (
                self._meta.resource_name,
                trailing_slash()),
                self.wrap_view('set_comments'),
                name="api_movie_set_comments"),
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
            raise NotFound('Movie does not exist')

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
            raise NotFound('Movie does not exist')

        request.user.remove_movie(movie)

        result = {
            'ok': True,
        }

        return self.create_response(request, result)

    def set_status(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        self.is_authenticated(request)

        try:
            raw_json = json.loads(request.body)
        except ValueError:
            raise BadRequest('Invalid json')

        status = raw_json.get('status')
        if status not in {constants.IGNORED, constants.PLAN_TO_WATCH, constants.WATCHED}:
            raise BadRequest('Invalid status')

        try:
            movie = Movie.objects.get(pk=raw_json.get('movie_id'))
        except Movie.DoesNotExist:
            raise NotFound('Movie does not exist')

        u2m = request.user.get_movie_status(movie)
        if u2m is None:
            request.user.add_movie(movie, status)
        else:
            request.user.remove_movie(movie)
            request.user.add_movie(movie, status)

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

        if int(score) != score:
            raise BadRequest('Invalid score')

        try:
            movie = Movie.objects.get(pk=raw_json.get('movie_id'))
        except Movie.DoesNotExist:
            raise NotFound('Movie does not exist')

        request.user.set_movie_score(movie, score)

        result = {
            'ok': True,
        }

        return self.create_response(request, result)

    def set_comments(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        self.is_authenticated(request)

        try:
            raw_json = json.loads(request.body)
        except ValueError:
            raise BadRequest('Invalid json')

        comments = raw_json.get('comments')

        try:
            movie = Movie.objects.get(pk=raw_json.get('movie_id'))
        except Movie.DoesNotExist:
            raise NotFound('Movie does not exist')

        try:
            request.user.set_movie_comments(movie, comments)
        except request.user.CommentTooLong:
            raise BadRequest('Comment is too long')
        except request.user.CannotCommentUnwatchedMovie:
            raise BadRequest('Must mark movie as `Watched` first')

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
            raise NotFound('Movie does not exist')

        u2m = request.user.get_movie_status(movie)

        if u2m:
            result = {
                'status': u2m.status,
                'score': int(u2m.score) if u2m.score else None,
                'comments': u2m.comments,
                'id': u2m.id,
            }
        else:
            result = None

        return self.create_response(request, result)
