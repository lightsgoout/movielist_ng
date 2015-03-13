from tastypie import fields
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource
from movies.models import Genre


class GenreResource(ModelResource):
    name = fields.CharField(readonly=True)

    class Meta:
        queryset = Genre.objects.all()
        resource_name = 'movie'
        authentication = SessionAuthentication()
        authorization = Authorization()
        list_allowed_methods = ['get']

        fields = [
            'id',
            'name',
        ]

    def dehydrate_name(self, bundle):
        return bundle.obj.name
