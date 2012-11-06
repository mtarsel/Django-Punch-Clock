from django.conf.urls import patterns, include, url
import django.contrib.auth
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
     url(r'^$', 'punchclock.views.index', name='index'),
     url(r'^manage/$', 'management.views.manage', name='manage'),
     url(r'^clockin/$', 'punchclock.views.clockin', name='clockin'),

     #url(r'^punchclock/$', 'punchclock.views.index', name='index'),
     #url(r'^login/$', 'auth.views.login_user'),
     url(r'^manage_login/$', 'django.contrib.auth.views.login',name="login_user"),
     #url(r'^punchclock/clockin/$', 'punchclock.views.clockIn', name='clockIn'),
     url(r'^admin/', include(admin.site.urls)),
)
