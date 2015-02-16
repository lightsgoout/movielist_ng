from django.conf.urls import patterns, include
from django.conf.urls import url

urlpatterns = patterns('',
    url(r'^login/$', 'accounts.views.login_page', name='login'),
    url(r'^logout/$', 'accounts.views.logout_view', name='logout'),
    url(r'', include('registration.backends.default.urls')),
)
