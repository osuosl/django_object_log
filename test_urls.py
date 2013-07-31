from django.conf.urls import patterns, url, include

urlpatterns = patterns('',
    (r'^', include('object_log.urls')),
)
