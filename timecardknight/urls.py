from django.conf.urls import patterns, include, url
import django.contrib.auth
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
     url(r'^$', 'punchclock.views.clockin', name='index'),
     url(r'^clockin/$', 'punchclock.views.clockin', name='clockin'),
     url(r'^clockout/$', 'punchclock.views.clockout', name='clockout'),
     
     url(r'^manage_login/$', 'django.contrib.auth.views.login', name="login_user"),
     url(r'^manage/$', 'management.views.manage', name='manage'),
     url(r'^reports/$', 'management.views.reports', name='reports'),
     url(r'^timecards/$', 'management.views.timecards', name='timecards'),

     url(r'^admin/', include(admin.site.urls)),
)
