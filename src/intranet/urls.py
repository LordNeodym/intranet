from django.conf.urls import include, url, patterns
from django.contrib import admin
from core import views
from django.conf import settings


urlpatterns = [
	url(r'^$', views.home, name='home'),
    url(r'^admin/', include(admin.site.urls)),
	url(r'^login/$', views.login, name='login'),
	url(r'^register/$', views.register, name='register'),
    url(r'^edit_profile/', views.edit_profile),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^rules/$', views.rules, name='rules'),
    url(r'^users/$', views.users, name='users'),
    url(r'^lan-archive/(?P<slug>[-\w\d]+)/$', views.lan_archive, name='lan_archive'),
    url(r'^off-topic/menu/$', views.menu, name='menu'),
    url(r'^off-topic/menu/(?P<slug>[-\w\d]+)/$', views.menu_order, name='menu_order'),
    url(r'^off-topic/menu/(?P<slug>[-\w\d]+)/(?P<command>[-_a-z]+)/$', views.menu_order, name='menu_order'),
    url(r'^off-topic/images/$', views.images, name='images'),
    url(r'^off-topic/videos/$', views.videos, name='videos'),
    url(r'^save_tournament_bracket$', views.save_tournament_bracket),
    url(r'^games/(?P<slug>[-\w\d]+)/$', views.game, name='game'),
    url(r'^games/(?P<slug>[-\w\d]+)/(?P<match_id>[\d]+)/$', views.match, name='match'),
    url(r'^games/(?P<slug>[-\w\d]+)/(?P<match_id>[\d]+)/(?P<command>[-_a-z]+)/$', views.match),
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