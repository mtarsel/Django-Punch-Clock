from django.conf.urls import patterns, include, url
import django.contrib.auth
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
     url(r'^$', 'punchclock.views.clockin', name='index'),
     url(r'^clockIn/$', 'punchclock.views.clockin', name='clockin'),
     url(r'^clockOut/$', 'punchclock.views.clockout', name='clockout'),
     url(r'^admin/', include(admin.site.urls)),
)