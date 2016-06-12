# ~*~ coding:utf-8 ~*~

from django.conf.urls import include, url
from django.conf import settings
from django.contrib import admin
from main.views import index

urlpatterns = [
    url(r'', index, name='index'),
]

from main.views.auth import (signin, signout, signup)
urlpatterns += [
    url(r'^signin/$', signin, name="signin"),
    url(r'^signup/$', signup, name="signup"),
    url(r'^signout/$', signout, name="signout")
]

