from django.conf.urls import patterns, url
from alan import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^grammar/$', views.grammar, name='grammar'),
]