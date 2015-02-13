from django.conf.urls import patterns, include, url
from main.feeds import LastFeed, PopularFeed

urlpatterns = patterns('',
    url(r'^$', 'main.views.index'),
    url(r'^baslik/(?P<title>[\w\W]+)', 'main.views.TitlePage'),
    url(r'^entry/(?P<entry_id>[\w\W]+)/$', 'main.views.EntryPage'),
    url(r'^arama/', 'main.views.SearchPage'),
    url(r'^enson', 'main.views.FeedPage'),
    url(r'^ajax/leftframe/$', 'main.views.refresh_left_frame'),
    url(r'^feed/populartitle/$', PopularFeed()),
    (r'^feed/enson', LastFeed()),
    url(r'^giris', 'main.views.LoginPage'),
    url(r'^auth', 'main.views.AuthView'),
    url(r'^cikis', 'main.views.Logout'),
    url(r'^kayit', 'main.views.RegisterUserPage'),
    url(r'^ajax/$', 'main.views.vote'),
    url(r'^remove/$', 'main.views.deleteentry'),
    url(r'^kullanici/(?P<user_name>[\w\W]+)', 'main.views.UserPage'),
    url(r'^entry/duzenle/(?P<id>\d+)', 'main.views.EditPage')
)
