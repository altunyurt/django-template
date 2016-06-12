# ~*~ coding:utf-8 ~*~

from django.conf.urls import include, url
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('main.urls')),
]

if settings.DEBUG:
    from django.views.static import serve
    urlpatterns = [
        url(r'^media/(?P<path>.*)', serve, {'document_root':settings.MEDIA_ROOT}),
    ] + urlpatterns
