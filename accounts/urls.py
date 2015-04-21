from django.conf.urls import patterns, include
from django.conf.urls import url

urlpatterns = patterns(
    '',
    url(r'^login/$', 'accounts.views.login_page', name='login'),
    url(r'^logout/$', 'accounts.views.logout_view', name='logout'),
    url(r'^settings/$', 'accounts.views.settings_personal', name='settings_personal'),
    url(r'^change_password/$', 'accounts.views.change_password', name='change_password'),
    url(r'^import/kinopoisk/$', 'imports.views.import_kinopoisk', name='import_kinopoisk'),
    url(r'^import/imdb/$', 'imports.views.import_imdb', name='import_imdb'),
    url(r'', include('registration.backends.default.urls')),
)
