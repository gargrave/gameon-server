from django.conf.urls import url

from . import views_games, views_platforms, views_tags

urlpatterns = [
    url(r'^games/?$', views_games.GameList.as_view()),
    url(r'^games/(?P<pk>[0-9]+)/?$', views_games.GameDetail.as_view()),

    url(r'^platforms/?$', views_platforms.PlatformList.as_view()),
    url(r'^platforms/(?P<pk>[0-9]+)/?$',
        views_platforms.PlatformDetail.as_view())
]
