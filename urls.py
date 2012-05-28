# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls.defaults import patterns, url, include
from django.contrib.auth.views import login, logout
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap as djsitemap


from cards import views as card_view
from cards.views import CardDetailView
from feeds.models import LastCardsFeed
from sitemap.models import CardsSitemap, CategorySitemap, TagSitemap
from users import views as users_view


sitemaps = {
    'topic' : CardsSitemap,
    'categories' : CategorySitemap,
    'tags' : TagSitemap,
}


admin.autodiscover()

urlpatterns = patterns('',
    # Главная страница
    url(r'^$', card_view.index),
    url(r'^category/(?P<category_slug>[\w-]+)/$',
        card_view.index,
        name='category'),
    url(r'^category/(?P<category_slug>[\w-]+)/(?P<tag_slug>[\w-]+)/$',
        card_view.index,
        name='tag'),
    # Подробная страница
    url(r'^(?P<pk>\d+)/?$', CardDetailView.as_view(), name='details'),
    url(r'^details/(?P<slug>[\w-]+)?$',
         CardDetailView.as_view(),
         name='details_slug'),

    # логин и регистариция.
    url(r'^login/', login),
    url(r'^logout/', logout, {'next_page': '/' }),
    # url связанные с пользователями.
    url(r'^user/(?P<username>[\d\w_]+)/?$', users_view.details, name="user_details"),
    url(r'^settings/$', users_view.edit),
    # RSS
    url(r'^feeds/latest/$', LastCardsFeed(), name='feeds_latest'),
    # the sitemap
    (r'^sitemap.xml$', djsitemap, {'sitemaps': sitemaps}),
    # админка
    (r'^admin/', include(admin.site.urls)),
)

if getattr(settings, 'DJANGO_SERVE_STATIC', False):
    urlpatterns += patterns('',
        (r'^'+settings.MEDIA_URL.strip('/')+'/(?P<path>.*)$',
                                                   'django.views.static.serve',
                                       {'document_root': settings.MEDIA_ROOT}),

    )


