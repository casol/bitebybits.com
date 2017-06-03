from django.contrib.sitemaps import Sitemap
from .models import Post


class PostSitemap(Sitemap):
    # Change frequency
    changefreq = 'monthly'
    # max=1
    priority = 0.9

    def items(self):
        """Return published entries."""
        return Post.published.all()

    def lastmod(self, obj):
        """Return last modification of a post."""
        return obj.publish
