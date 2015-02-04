from django.conf.urls import patterns, include, url
from main.feeds import LastFeed

urlpatterns = patterns('',
    url(r'^$', 'main.views.index'),
    url(r'^baslik/(?P<title>[\w\W]+)', 'main.views.TitlePage'),
    url(r'^entry/(?P<entry_id>[\w\W]+)', 'main.views.EntryPage'),
    url(r'^arama/', 'main.views.SearchPage'),
    url(r'^enson', 'main.views.FeedPage'),
    (r'^feed/enson', LastFeed()),
    url(r'^giris-yap', 'main.views.LoginPage'),
    url(r'^auth', 'main.views.AuthView'),
    url(r'^cikis', 'main.views.Logout'),
    url(r'^kayit', 'main.views.RegisterUserPage'),
    url(r'^ajax/', 'main.views.vote'),
    url(r'^kullanici/(?P<user_name>[\w\W]+)', 'main.views.UserPage')
)
