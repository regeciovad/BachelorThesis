from django.conf.urls import url
from alan import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^grammar/$', views.grammar, name='grammar'),
    url(r'^lrtable/$', views.lrtable, name='lrtable'),
    url(r'^ahlrtable/$', views.ad_hoc_lrtable, name='ahlrtable'),
    url(r'^scanner/$', views.run_scanner, name='scanner'),
    url(r'^parser/$', views.run_parser, name='parser'),
    url(r'^panic_mode/$', views.run_panic_mode_parser, name='panic_mode'),
    url(r'^panic_mode_first/$', views.run_panic_mode_parser_first, name='panic_mode_first'),
    url(r'^ad_hoc/$', views.run_parser_ad_hoc, name='ad_hoc'),
    url(r'^alan_mode/$', views.run_alan_mode_parser, name='alan_mode'),
    url(r'^comparison/$', views.comparison, name='comparison'),
    url(r'^man/$', views.man, name='man'),
    url(r'^download/$', views.download, name='download'),
    url(r'^changelog/$', views.changelog, name='changelog'),
]
