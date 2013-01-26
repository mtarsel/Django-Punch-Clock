from django.contrib import admin
from punchclock.models import *
from django.conf.urls import patterns, include, url
from django.http import *


admin.site.register(Account)
admin.site.register(Department)

def generate_timecards(modeladmin, request, queryset):
	queryset.update(status='g')
	generate_timecards.short_description = "Select students to generate Timecards for"
	selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
	ct = ContentType.objects.UserAdmin(queryset.model)
	return HttpResponseRedirect("/timecards/?ct=%s&ids=%s" % (ct.pk, ",".join(selected)))
	#STILL WRITING THIS VIEW. JUST TRYING TO GET AND ADMIN ACTION

class UserAdmin(admin.ModelAdmin):
	
	fields = ['first_name', 'last_name', 'number', 'pay_rate', 'start_date', 'amount_paid', 'department', 'account' ]
	actions = [generate_timecards]
	#SAYS generate_timecards IS NOT DEFINED
	
admin.site.register(User, UserAdmin)