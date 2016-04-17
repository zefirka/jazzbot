from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^$', 'jazz.views.index'),
    url(r'^api/(?P<token>[0-9]{9}\:[0-9\w_]{35})/$', 'jazz.views.api')
]
