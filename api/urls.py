from django.conf.urls import *


urlpatterns = patterns('',
    url(r'^v1/', include('api.v1.urls')),
)
