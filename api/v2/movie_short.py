from django.core.urlresolvers import reverse
from tastypie import fields
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource
from movies.models import Movie


class MovieShortResource(ModelResource):
    title = fields.CharField(readonly=True)
    image_url = fields.CharField(readonly=True)
    page_url = fields.CharField(readonly=True)

    class Meta:
        queryset = Movie.objects.all()
        resource_name = 'movie_short'
        authentication = Authentication()
        authorization = Authorization()
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        include_resource_uri = False

        fields = [
            'id',
            'year',
            'title',
            'page_url',
            'rating_imdb',
            'rating_metacritic',
            'rating_tomatoes',
            'votes_imdb',
        ]

    def dehydrate_title(self, bundle):
        return bundle.obj.title

    def dehydrate_image_url(self, bundle):
        return bundle.obj.image_url

    def dehydrate_page_url(self, bundle):
        return reverse(
            'movie',
            kwargs={'movie_id': bundle.obj.pk, 'slug': bundle.obj.slug})
