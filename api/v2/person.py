from django.core.urlresolvers import reverse
from tastypie import fields
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource
from movies.models import Person


class PersonResource(ModelResource):
    name = fields.CharField(readonly=True)
    page_url = fields.CharField(readonly=True)

    class Meta:
        queryset = Person.objects.all()
        resource_name = 'people'
        authentication = SessionAuthentication()
        authorization = Authorization()
        list_allowed_methods = ['get']
        include_resource_uri = False

        fields = [
            'name',
            'page_url',
            'sort_power',
        ]

    def dehydrate_name(self, bundle):
        return bundle.obj.name

    def dehydrate_page_url(self, bundle):
        return reverse(
            'person',
            kwargs={'person_id': bundle.obj.pk, 'slug': bundle.obj.slug})
