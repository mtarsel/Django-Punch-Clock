from django.contrib import admin
from punchclock.models import *
from django.conf.urls import patterns, include, url


admin.site.register(Account)
admin.site.register(Department)

#this displays the CHANGE USER field for user. 
class UserAdmin(admin.ModelAdmin):
	
	fields = ['first_name', 'last_name', 'number', 'pay_rate', 'start_date', 'amount_paid', 'department', 'account' ]
	
	def generate_timecards(modeladmin, request, queryset):
		queryset.update(status='g')
		generate_timecards.short_description = "Mark Students to generate Timecards for"
		
		#I HAVE CODE TO MAKE THE PDF WITH USER VALUES IN MODEL (ITS THE LARGE COMMENTED MODEL NAMED GenerateTimecard

admin.site.register(User, UserAdmin)

		
		
