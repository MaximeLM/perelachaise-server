# -*- coding: utf8 -*-

from django.conf.urls import patterns, url

from test_application import views

urlpatterns = patterns('',
    url(r'^monumentall/nodeOSM/(?P<name>\w+)$', views.monumentall_nodeOSM, name='monumentall_nodeOSM'),
)
