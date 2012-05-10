# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls.defaults import patterns, url, include
from django.contrib.auth.views import login, logout
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap as djsitemap
from django.contrib.syndication.views import feed as sfeed


from cards import views as card_view
from feeds.models import LastCards
from sitemap.models import CardsSitemap
from users import views as users_view


feeds = {
    'latest': LastCards,
}
sitemaps = {
    'topic' : CardsSitemap
}


admin.autodiscover()

urlpatterns = patterns('',
    # Главная страница
    url(r'^$', card_view.index),
    # Подробная страница
    url(r'^(\d+)/?$', card_view.details, name='details'),
    url(r'^edit/(\d+)/?$', card_view.edit),
    url(r'^favorites/$', card_view.favorites),
    url(r'^favorites/add/(?P<card_id>\d+)$', card_view.fav_add),
    url(r'^favorites/del/(?P<card_id>\d+)$', card_view.fav_del),
    url(r'^usefull/$', card_view.rating ),
    # поиск
    url(r'^search/$', card_view.search),
    # логин и регистариция.
    url(r'^login/', login),
    url(r'^logout/', logout, {'next_page': '/' }),
    url(r'^register/', users_view.register),
    # url связанные с пользователями.
    url(r'^user/(?P<username>[\d\w_]+)/?$', users_view.details),
    url(r'^settings/$', users_view.edit),
    # RSS
    (r'^feeds/(?P<url>.*)/$', sfeed, {'feed_dict': feeds}),
    # the sitemap
    (r'^sitemap.xml$', djsitemap, {'sitemaps': sitemaps}),
    # админка
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
)

if getattr(settings, 'DJANGO_SERVE_STATIC', False):
    urlpatterns += patterns('',
        (r'^'+settings.MEDIA_URL.strip('/')+'/(?P<path>.*)$',
                                                   'django.views.static.serve',
                                       {'document_root': settings.MEDIA_ROOT}),

    )


