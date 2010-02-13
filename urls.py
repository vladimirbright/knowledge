# -*- coding: utf8 -*-

from django.conf.urls.defaults import *
from django.contrib import admin#, admindocs
from django.contrib.auth.views import login, logout

from django.conf import settings

from knowledge.cards import views as card_view
from knowledge.users import views as users_view

admin.autodiscover()

urlpatterns = patterns('',
    # Главная страница
    url(r'^$', card_view.index),
    # Подробная страница
    url(r'^(\d+)/?$', card_view.details),
    url(r'^favorites/$', card_view.favorites),
    url(r'^favorites/add/(?P<card_id>\d+)$', card_view.fav_add),
    url(r'^favorites/del/(?P<card_id>\d+)$', card_view.fav_del),
    url(r'^usefull/$', card_view.rating),

    # TODO не забыть убрать обработку статики с джанги.
    (r'^s/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

    # комментарии стандартные джанговские.
    (r'^comments/', include('django.contrib.comments.urls')),

    url(r'^login/', login),
    url(r'^logout/', logout),
    url(r'^register/', users_view.register),

    #(r'^users/', include('knowledge.users.urls')),

    (r'^admin/', include(admin.site.urls)),
    #(r'^admin/doc/', include(admindocs.site.urls)),

)
