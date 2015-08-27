from django.conf.urls import include, url
from django.contrib import admin
from core import views


urlpatterns = [
	url(r'^$', views.home, name='home'),
    url(r'^admin/', include(admin.site.urls)),
	url(r'^login/$', views.login, name='login'),
	url(r'^register/$', views.register, name='register'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^rules/(?P<slug>[-\w\d]+)/$', views.rules, name='rules'),
    url(r'^pictures/$', views.pictures, name='pictures'),
    url(r'^movies/$', views.movies, name='movies'),
    url(r'^games/(?P<slug>[-\w\d]+)/$', 'core.views.game_site'),
]
