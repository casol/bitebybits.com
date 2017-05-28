from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Post


class LatestPostFeed(Feed):
    """
    Django built-in syndication feed framework to generate
    RSS or Atom feeds.
    """
    title = 'Bite by Bits - Blog'
    link = '/blog/'
    description = 'New post on Bite by Bits!'

    def items(self):
        return Post.published.all()[:3]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.body, 30)
