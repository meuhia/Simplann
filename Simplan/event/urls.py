# coding: utf-8

from django.conf.urls import patterns, url

import views


urlpatterns = patterns('',
    url(r'^editer/(?P<evt_id>.+)/$', views.edit_event),
    #url(r'^participer/(?P<evt_id>.+)/$', views.view_event),
    url(r'^retirer/(?P<evt_id>.+)/$', views.del_makechoices),
    url(r'^terminer/(?P<evt_id>.+)/$', views.end_event),
    url(r'^inviter_terminer/(?P<evt_id>.+)/$', views.invit_end_event),
    url(r'^choisir/(?P<evt_id>.+)/$', views.make_choice),
    url(r'^recapitulatif/(?P<evt_id>.+)/$', views.recap_event),
    
    url(r'^options/nouveau/(?P<evt_id>.+)/$', views.new_option),
    url(r'^options/editer/(?P<opt_id>.+)$', views.edit_option),
    url(r'^options/up/(?P<opt_id>.+)$', views.up_option),
    url(r'^options/down/(?P<opt_id>.+)$', views.down_option),
    url(r'^options/supprimer/(?P<opt_id>.+)$', views.del_option),
    
    url(r'^choix/nouveau/(?P<opt_id>.+)/$', views.new_choice),
    url(r'^choix/editer/(?P<opt_id>.+)/(?P<ch_id>.+)$', views.edit_choice),
    url(r'^choix/supprimer/(?P<ch_id>.+)$', views.del_choice),
    url(r'^choix/modifier/$', views.modify_choice),
)
