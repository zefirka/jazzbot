from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from jazz.service import login, add, signOut, remove

urlpatterns = [
    url(r'^$', 'jazz.views.index'),
    url(r'^admin$', 'jazz.views.adminka'),
    url(r'^login$', login),
    url(r'^add$', add),
    url(r'^out$', signOut),
    url(r'^remove$', remove),
    url(r'^api/(?P<token>[0-9]{9}\:[0-9\w_\-]{35})/$', 'jazz.views.api')
]

urlpatterns += staticfiles_urlpatterns()