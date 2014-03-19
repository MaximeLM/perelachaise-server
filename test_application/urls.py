# -*- coding: utf8 -*-

from django.conf.urls import patterns, url

from test_application import views

urlpatterns = patterns('',
    url(r'^monumentall/nodeOSM/(?P<name>\w+)$', views.monumentall_nodeOSM, name='monumentall_nodeOSM'),
    url(r'^monumentall/personnalite/(?P<name>\w+)$', views.monumentall_personnalite, name='monumentall_personnalite'),
    url(r'^monumentall/monument/(?P<name>\w+)$', views.monumentall_monument, name='monumentall_monument'),
)
