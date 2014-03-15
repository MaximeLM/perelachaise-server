from django.conf.urls import patterns, url

from webservice import views

urlpatterns = patterns('',
    url(r'^monument/all/$', views.monument_all, name='monument_all'),
)
