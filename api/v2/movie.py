from django.core.urlresolvers import reverse
from django.conf.urls import url
from tastypie import fields
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import Authorization
from tastypie.constants import ALL_WITH_RELATIONS
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash
from api.v2.country import CountryResource
from api.v2.genre import GenreResource
from api.v2.person import PersonResource
from movies.models import Movie
from suggestions.base import AbstractSuggester


class MovieResource(ModelResource):
    title = fields.CharField(readonly=True)
    image_url = fields.CharField(readonly=True)
    page_url = fields.CharField(readonly=True)
    genres = fields.ManyToManyField(
        GenreResource,
        'genres',
        full=False,
        null=True,
        readonly=True
    )
    countries = fields.ManyToManyField(
        CountryResource,
        'countries',
        full=True,
        null=True,
        readonly=True,
    )
    directors = fields.ManyToManyField(
        PersonResource,
        'directors',
        full=True,
        null=True,
        readonly=True,
    )
    cast = fields.ManyToManyField(
        PersonResource,
        'cast',
        full=True,
        null=True,
        readonly=True,
    )
    composers = fields.ManyToManyField(
        PersonResource,
        'composers',
        full=True,
        null=True,
        readonly=True,
    )

    class Meta:
        queryset = Movie.objects.all()
        resource_name = 'movie'
        authentication = SessionAuthentication()
        authorization = Authorization()
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        filtering = {
            'cast': ALL_WITH_RELATIONS,
            'directors': ALL_WITH_RELATIONS,
            'composers': ALL_WITH_RELATIONS,
        }

        fields = [
            'id',
            'year',
            'title',
            'page_url',
            'rating_imdb',
            'rating_metacritic',
            'rating_tomatoes',
            'tomatoes_fresh',
            'director',
        ]

    def dehydrate_title(self, bundle):
        return bundle.obj.title

    def dehydrate_image_url(self, bundle):
        return bundle.obj.image_url

    def dehydrate_page_url(self, bundle):
        return reverse('movie', kwargs={'movie_id': bundle.obj.pk})

    def dehydrate_genres(self, bundle):
        return [g for g in bundle.obj.genres.all()]

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/get_suggestions%s$" % (
                self._meta.resource_name,
                trailing_slash()),
                self.wrap_view('get_suggestions'),
                name="api_get_suggestions"),
        ]

    def get_suggestions(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)

        suggester = AbstractSuggester()
        object_list = suggester.get_suggestion_list(request.user)
        objects = []
        for index, result in enumerate(object_list):
            movie, factor = result
            bundle = self.build_bundle(obj=movie, request=request)
            bundle = self.full_dehydrate(bundle)
            bundle.data['suggestion_factor'] = factor
            bundle.data['suggestion_order'] = index
            objects.append(bundle)

        json_object_list = {
            'objects': objects,
        }

        return self.create_response(request, json_object_list)

