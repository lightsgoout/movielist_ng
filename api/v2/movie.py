from django.core.urlresolvers import reverse
from tastypie import fields
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource
from movies.models import Movie


class MovieResource(ModelResource):
    title = fields.CharField(readonly=True)
    image_url = fields.CharField(readonly=True)
    movie_page_url = fields.CharField(readonly=True)

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
            'image_url',
        ]

    def dehydrate_title(self, bundle):
        return bundle.obj.title

    def dehydrate_image_url(self, bundle):
        return bundle.obj.image_url

    def dehydrate_movie_page_url(self, bundle):
        return reverse('movie', kwargs={'movie_id': bundle.obj.pk})


