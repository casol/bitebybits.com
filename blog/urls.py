from django.conf.urls import url

from .feeds import LatestPostFeed
from . import views


urlpatterns = [
    url(r'^$',
        views.post_list,
        name='post_list'),

    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<post>[-\w]+)/$',
        views.post_detail,
        name='post_detail'),

    url(r'^tag/(?P<tag_slug>[-\w]+)/$',
        views.post_list,
        name='post_list_by_tag'),

    # Feeds
    url(r'^feed/$',
        LatestPostFeed(),
        name='post_feed'),

]
