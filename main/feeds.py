import datetime
from django.contrib.syndication.views import Feed
from main.models import Entry

class LastFeed(Feed):
    title = 'En son yazilan entryler (Feed)'
    description = 'En son yazilan entryler (Feed)'
    link = ""

    def items(self):
        return Entry.objects.filter().order_by('-pub_date')[:15]

    def item_link(self, item):
        return "/entry/{}".format(item.id)

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item

class PopularFeed(Feed):
    title = "Popular titles"
    description = "Popular titles"
    link = ""

    def items(self):
        #PopularFeeds
        from collections import OrderedDict
        from operator import itemgetter
        today_entries = Entry.objects.filter(pub_date__year=datetime.date.today().year,
                                              pub_date__month=datetime.date.today().month,
                                              pub_date__day=datetime.date.today().day)
        today_hits = {}
        for entry in today_entries:
            if str(entry.title) in today_hits.keys():
                today_hits[entry.title] += 1
            else:
                today_hits.update({entry.title: 1})


        hits = list(OrderedDict(sorted(today_hits.items(), key=itemgetter(1), reverse=True)))
        return hits[:15]

    def item_link(self, item):
        return "/baslik/{}".format(item)

    def item_title(self, item):
        return item

    def item_description(self, item):
        return item