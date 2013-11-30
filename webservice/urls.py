from django.conf.urls import patterns, url

from webservice import views

urlpatterns = patterns('',
    url(r'^tombe/$', views.tombe, name='tombe'),
)
