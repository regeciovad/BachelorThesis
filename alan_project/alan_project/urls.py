from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^$', 'alan.views.about', name='about'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^alan/', include('alan.urls')),
]
