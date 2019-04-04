from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from blog.models import BlogEntry

class LatestEntriesRssFeed(Feed):
    title = "My Special Blog"
    link = "/blog/"
    description = "The last ten posts from My Special Blog."

    def items(self):
        items = BlogEntry.published_objects.all().order_by('-id')[:10]
        return items

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.body
    
    def item_link(self, item):
        return "/blog/%s" % item.slug
        
class LatestEntriesAtomFeed(LatestEntriesRssFeed):
    feed_type = Atom1Feed
    subtitle = LatestEntriesRssFeed.description
