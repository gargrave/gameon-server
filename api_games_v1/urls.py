from django.conf.urls import url

from . import views_games, views_tags

urlpatterns = [
    url(r'^games/?$', views_games.GameList.as_view()),
    url(r'^games/(?P<pk>[0-9]+)/?$', views_games.GameDetail.as_view()),

    url(r'^tags/?$', views_tags.TagList.as_view()),
    url(r'^tags/add/?$', views_tags.TagGameRelationCreateView.as_view()),
    url(r'^tags/remove/?$', views_tags.TagGameRelationDeleteView.as_view()),
    url(r'^tags/delete/(?P<pk>[0-9]+)/?$', views_tags.TagDeleteView.as_view()),
]
