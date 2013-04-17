from django.conf.urls import patterns, include, url
import django.contrib.auth
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
     url(r'^$', 'punchclock.views.clockin', name='index'),
     url(r'^clockIn/$', 'punchclock.views.clockin', name='clockin'),
     url(r'^clockOut/$', 'punchclock.views.clockout', name='clockout'),
     url(r'^timecards$', 'punchclock.views.timecards', name='timecards'),
         #url(r'^generate_timecards/$', 'punchclock.views.generate_timecards', name='generate_timecards'),
         #url(r'^admin/generate_timecards/$', TemplateView.as_view(template_name='admin/generate_timecards.html')),
     url(r'^admin/', include(admin.site.urls)),
)