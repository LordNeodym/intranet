from django.conf.urls import include, url, patterns
from django.contrib import admin
from core import views
from django.conf import settings


urlpatterns = [
	url(r'^$', views.home, name='home'),
    url(r'^admin/', include(admin.site.urls)),
	url(r'^login/$', views.login, name='login'),
	url(r'^register/$', views.register, name='register'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^rules/(?P<slug>[-\w\d]+)/$', views.rules, name='rules'),
    url(r'^off-topic/menu/$', views.menu, name='menu'),
    url(r'^off-topic/images/$', views.images, name='images'),
    url(r'^off-topic/videos/$', views.videos, name='videos'),
    url(r'^games/(?P<slug>[-\w\d]+)/$', views.game_site, name='games'),
    url(r'^games/(?P<slug>[-\w\d]+)/(?P<command>[-_a-z]+)/$', views.game_site),
]


if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
        }),
)