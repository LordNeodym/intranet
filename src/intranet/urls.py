from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
	url(r'^$', 'core.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
	url(r'^(?P<slug>[-\w\d]+)/$', 'core.views.game_site'),
]