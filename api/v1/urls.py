from django.conf.urls import *


urlpatterns = patterns('',
    # API urls
    url(r'^add_to_list/(?P<movie_id>[\d]+)/(?P<status>[W,P,I])/$', 'api.v1.views.add_to_list'),
    url(r'^suggest_another_movie/(?P<movie_id>[\d]+)/(?P<status>[W,P,I])/$', 'api.v1.views.suggest_another_movie'),
)
