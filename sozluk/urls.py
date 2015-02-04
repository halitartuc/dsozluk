from django.conf.urls import patterns, include, url
from django.contrib import admin
import main.tr.url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sozluk.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(main.tr.url))
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
