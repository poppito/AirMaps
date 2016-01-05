from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
	url(r'^$', 'Airmap.views.getHome'),
	url(r'/^$', 'Airmap.views.getHome'),
	url(r'^getLocation$', 'Airmap.views.getLocation'),
	url(r'^getMap$', 'Airmap.views.getMap'),
)
