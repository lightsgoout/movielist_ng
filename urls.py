from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
# from ajax_select import urls as ajax_select_urls
# from api import urls as api_urls
admin.autodiscover()

# js_info_dict = {
#     'domain': 'djangojs',
#     'packages': ('app',),
# }

urlpatterns = patterns('',
    url(r'^$', 'movies.views.index'),
    url(r'', include('social_auth.urls')),
    url(r'', include('movies.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/lookups/', include('ajax_select.urls')),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^api/', include('api.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^add/$', 'movies.views.wizard', name='wizard'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    # url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),
)
