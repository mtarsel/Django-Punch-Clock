from django.conf.urls import patterns, include, url
import django.contrib.auth
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
     url(r'^$', 'punchclock.views.clockIn', name='index'),
     url(r'^clockin/$', 'punchclock.views.clockIn', name='clockIn'),
     url(r'^clockout/$', 'punchclock.views.clockOut', name='clockOut'),
     url(r'^timecards/$', 'punchclock.views.timecards', name='timecards'),
     url(r'^admin/', include(admin.site.urls)),
)
