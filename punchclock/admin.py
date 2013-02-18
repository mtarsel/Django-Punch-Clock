from django.contrib import admin
from punchclock.models import *
from django.conf.urls import patterns, include, url
from django.http import *

admin.site.register(Account)
admin.site.register(Department)

def generate_timecards(modeladmin, request, queryset):
	generate_timecards.short_description = "Select students to generate Timecards for"
	selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
	#ct = ContentType.objects.UserAdmin(queryset.model)
	#return HttpResponseRedirect("/timecards/?ct=%s&ids=%s" % (ct.pk, ",".join(selected)))
	return HttpResponseRedirect( '/generate_timecards.html' )

class UserAdmin(admin.ModelAdmin):
	fields = ['first_name', 'last_name', 'number', 'pay_rate', 'start_date', 'amount_paid', 'department', 'account', 'active' ]
	actions = [generate_timecards]
		
	def get_urls(self):
		urls = super(UserAdmin, self).get_urls()
		my_urls = patterns('',
			(r'^construct_timecards/$', 'punchclock.views.construct_timecards')
		)
		return my_urls + urls
	
admin.site.register(User, UserAdmin)