from tastypie import fields
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource
from common.models import Country


class CountryResource(ModelResource):
    name = fields.CharField(readonly=True)

    class Meta:
        queryset = Country.objects.all()
        resource_name = 'country'
        authentication = SessionAuthentication()
        authorization = Authorization()
        list_allowed_methods = ['get']
        include_resource_uri = False

        # TODO: store iso data at the frontend, don't send it via API.
        fields = [
            'name',
            'iso_code',
        ]

    def dehydrate_name(self, bundle):
        return bundle.obj.name
