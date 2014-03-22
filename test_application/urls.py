# -*- coding: utf8 -*-

from django.conf.urls import patterns, url

from test_application import views

urlpatterns = patterns('',
    url(r'^fixtures/monumentall/nodeOSM/(?P<name>\w+)$', views.fixtures_monumentall_nodeOSM, name='fixtures_monumentall_nodeOSM'),
    url(r'^fixtures/monumentall/personnalite/(?P<name>\w+)$', views.fixtures_monumentall_personnalite, name='fixtures_monumentall_personnalite'),
    url(r'^fixtures/monumentall/monument/(?P<name>\w+)$', views.fixtures_monumentall_monument, name='fixtures_monumentall_monument'),
    
    url(r'^monument/all/$', views.monument_all, name='monument_all'),
    
    url(r'^truc/monument/all/$', views.monument_all, name='monument_all1'),
    url(r'^monument/all/truc/$', views.monument_all, name='monument_all2'),
    url(r'^truc/$', views.monument_all, name='monument_all3'),
    
    url(r'^fixtures/webservice/$', views.fixtures_test_webservice, name='fixtures_test_webservice'),
)
