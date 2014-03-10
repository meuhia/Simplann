# coding: utf-8

from django.conf.urls import patterns, url

import views


urlpatterns = patterns('',

    url(r'^apropos$', views.about),

    url(r'^$', views.home),
)
