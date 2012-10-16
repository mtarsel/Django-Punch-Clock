from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
     url(r'^manage/$', 'management.views.manage', name='manage'),
	 url(r'^index/$', 'punchclock.views.index', name='index'),
     url(r'^punchclock/$', 'punchclock.views.index', name='index'),
     #url(r'^index','views.home'),
     #url(r'^sitemap\.xml','views.sitemap'),
     #url(r'^movies/', include('movies.urls')),
     #url(r'^admin/', include(admin.site.urls)),
     #url(r'^search/',include('search.urls'))
 
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

     url(r'^admin/', include(admin.site.urls)),
)
