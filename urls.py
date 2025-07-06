# -*- coding: utf-8 -*-

from django.conf import settings
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
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

urlpatterns = [
    # Главная страница
    path('', card_view.index, name='index'),
    path('category/<slug:category_slug>/',
        card_view.index,
        name='category'),
    path('category/<slug:category_slug>/<slug:tag_slug>/',
        card_view.index,
        name='tag'),
    # Подробная страница
    path('<int:pk>/', CardDetailView.as_view(), name='details'),
    path('details/<slug:slug>/',
         CardDetailView.as_view(),
         name='details_slug'),

    # логин и регистариция.
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    # url связанные с пользователями.
    path('user/<str:username>/', users_view.details, name="user_details"),
    path('settings/', users_view.edit, name='settings'),
    # RSS
    path('feeds/latest/', LastCardsFeed(), name='feeds_latest'),
    # the sitemap
    path('sitemap.xml', djsitemap, {'sitemaps': sitemaps}, name='sitemap'),
    # админка
    path('admin/', admin.site.urls),
]

# Serve static and media files during development
if settings.DEBUG:
    from django.conf.urls.static import static
    from django.views.static import serve
    
    # Serve static files
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    
    # Serve media files
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


