# -*- coding: utf8 -*-

from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib.auth.views import login, logout

from knowledge.cards import views as card_view
from knowledge.users import views as users_view

admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', card_view.index),
    (r'^cards/', include('knowledge.cards.urls')),
    (r'^login/', login),
    (r'^logout/', logout),
    (r'^register/', users_view.register),
    #(r'^users/', include('knowledge.users.urls')),

    (r'^admin/', include(admin.site.urls)),
)
