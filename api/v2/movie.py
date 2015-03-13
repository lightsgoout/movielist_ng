from django.core.urlresolvers import reverse
from tastypie import fields
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource
from api.v2.country import CountryResource
from api.v2.genre import GenreResource
from api.v2.person import PersonResource
from movies.models import Movie


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

    class Meta:
        queryset = Movie.objects.all()
        resource_name = 'movie'
        authentication = SessionAuthentication()
        authorization = Authorization()
        list_allowed_methods = ['get']

        fields = [
            'id',
            'year',
            'title',
            'page_url',
            'rating_imdb',
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
