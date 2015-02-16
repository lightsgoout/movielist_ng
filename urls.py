from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
# from ajax_select import urls as ajax_select_urls
# from api import urls as api_urls
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'movies.views.index'),
    url(r'', include('social_auth.urls')),
    url(r'', include('movies.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/lookups/', include('ajax_select.urls')),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^api/', include('api.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^wizard/$', 'movies.views.wizard', name='wizard'),
)
