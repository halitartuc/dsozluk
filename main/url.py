from django.conf.urls import patterns, include, url
from main.feeds import LastFeed, PopularFeed

urlpatterns = patterns('',
    url(r'^$', 'main.views.index'),
    url(r'^baslik/(?P<title>[\w\W]+)', 'main.views.TitlePage'),
    url(r'^entry/(?P<entry_id>[\w\W]+)/$', 'main.views.EntryPage'),
    url(r'^arama/', 'main.views.SearchPage'),
    url(r'^ajax/leftframe/$', 'main.views.refresh_left_frame'),
    url(r'^feed/populartitle/$', PopularFeed()),
    url(r'^feed/enson', LastFeed()),
    url(r'^ajax/$', 'main.views.vote'),
    url(r'^remove/$', 'main.views.deleteentry'),
    url(r'^kullanici/(?P<user_name>[\w\W]+)', 'main.views.UserPage'),
    url(r'^entry/duzenle/(?P<id>\d+)', 'main.views.EditPage'),
    url(r'^ajax/search', 'main.views.RealTimeSearch'),
)
