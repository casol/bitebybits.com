from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Post


class LatestPostFeed(Feed):
    """
    Django built-in syndication feed framework to generate
    RSS or Atom feeds.
    """
    title = 'Blog-frombitstobytes'
    link = '/'
    description = 'New post on frombitstobytes.com!'

    def items(self):
        return Post.published.all()[:3]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.body, 30)
