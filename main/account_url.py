from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^login', 'main.views.LoginPage'),
    url(r'^auth', 'main.views.AuthView'),
    url(r'^logout', 'main.views.Logout'),
    url(r'^register', 'main.views.RegisterUserPage'),
    url(r'^password_change', 'main.views.ChangePassword'),
    url(r'^email_change', 'main.views.ChangeEmail'),
    url(r'^password_reset/$', 'django.contrib.auth.views.password_reset', name='password_reset'),
    url(r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        'django.contrib.auth.views.password_reset_confirm',
        name='password_reset_confirm'),
    url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete', name='password_reset_complete'),

)
