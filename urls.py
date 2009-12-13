# -*- coding: utf8 -*-
from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib.auth.views import login, logout

from django.conf import settings

from knowledge.cards import views as card_view
from knowledge.users import views as users_view

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', card_view.index),
    url(r'^(\d+)/?$', card_view.details),
    # TODO не забыть убрать обработку статики с джанги.
    (r'^s/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

    (r'^cards/', include('knowledge.cards.urls')),
    url(r'^login/', login),
    url(r'^logout/', logout),
    url(r'^register/', users_view.register),
    #(r'^users/', include('knowledge.users.urls')),

    (r'^admin/', include(admin.site.urls)),
)
