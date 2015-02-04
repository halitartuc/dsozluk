from django.contrib.syndication.views import Feed
from main.models import Entry

class LastFeed(Feed):
    title = 'En son yazilan entryler (Feed)'
    description = 'En son yazilan entryler (Feed)'
    link = ""

    def items(self):
        return Entry.objects.filter().order_by('-pub_date')[:25]

    def item_link(self, item):
        return "/entry/{}".format(item.id)

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item