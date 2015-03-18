from django.conf.urls import *


urlpatterns = patterns(
    '',
    url(r'^v2/', include('api.v2.urls')),
)
