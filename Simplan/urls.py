from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin

import event.views
import settings


admin.autodiscover()


urlpatterns = patterns('',
    url(r'^compte/', include('Simplan.account.urls')),
    url(r'^evenement/', include('Simplan.event.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',event.views.new_event),
    (r'^i18n/', include('django.conf.urls.i18n'))

)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.SERVE:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
