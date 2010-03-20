# -*- coding: utf8 -*-

from django.conf.urls.defaults import *
from django.contrib import admin#, admindocs
from django.contrib.auth.views import login, logout

from django.conf import settings

from knowledge.cards import views as card_view
from knowledge.users import views as users_view

admin.autodiscover()

urlpatterns = patterns('/mysite.fcgi/',
    # Главная страница
    url(r'^$', card_view.index),
    # Подробная страница
    url(r'^(\d+)/?$', card_view.details),
    url(r'^favorites/$', card_view.favorites),
    url(r'^favorites/add/(?P<card_id>\d+)$', card_view.fav_add),
    url(r'^favorites/del/(?P<card_id>\d+)$', card_view.fav_del),
    url(r'^usefull/$', card_view.rating ),
    # поиск
    url(r'^search/$', card_view.search),
    # комментарии стандартные джанговские.
    (r'^comments/', include('django.contrib.comments.urls')),
    # логин и регистариция.
    url(r'^login/', login),
    url(r'^logout/', logout, {'next_page': '/' }),
    url(r'^register/', users_view.register),
    # url связанные с пользователями.
    url(r'^user/(?P<username>[\d\w_]+)/?$', users_view.details),
    url(r'^settings/$', users_view.edit),
    # админка
    (r'^admin/', include(admin.site.urls)),
    #(r'^admin/doc/', include(admindocs.site.urls)),
)
