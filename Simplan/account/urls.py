# coding: utf-8

from django.conf.urls import patterns, url

import views


urlpatterns = patterns('',
    url(r'^$', views.index),
    url(r'^voir/(?P<user_name>.+)$', views.details),
    url(r'^mes_plans$', views.plans),

    url(r'^parametres/profil$', views.settings_profile),
    url(r'^parametres/compte$', views.settings_account),
    url(r'^parametres/user$', views.settings_user),

    url(r'^connexion$', views.login_view),
    url(r'^deconnexion/$', views.logout_view),
    url(r'^inscription$', views.register_view),
    url(r'^reinitialisation$', views.forgot_password),
    url(r'^new_password$', views.new_password),
    url(r'^activation$', views.active_account),
)
