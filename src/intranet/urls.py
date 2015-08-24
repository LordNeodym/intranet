from django.conf.urls import include, url
from django.contrib import admin
from core import views


urlpatterns = [
	url(r'^$', views.home, name='home'),
    url(r'^admin/', include(admin.site.urls)),
	url(r'^(?P<slug>[-\w\d]+)/$', 'core.views.game_site'),
	url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
]