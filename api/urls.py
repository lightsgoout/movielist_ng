from django.conf.urls import *


urlpatterns = patterns(
    '',
    url(r'^v1/', include('api.v1.urls')),
    url(r'^v2/', include('api.v2.urls')),
)
