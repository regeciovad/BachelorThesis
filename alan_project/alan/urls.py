from django.conf.urls import url
from alan import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^grammar/$', views.grammar, name='grammar'),
    url(r'^lrtable/$', views.lrtable, name='lrtable'),
    url(r'^scanner/$', views.run_scanner, name='scanner'),
    url(r'^parser/$', views.run_parser, name='parser'),
    url(r'^man/$', views.man, name='man'),
    url(r'^download/$', views.download, name='download'),
    url(r'^changelog/$', views.changelog, name='changelog'),
]
