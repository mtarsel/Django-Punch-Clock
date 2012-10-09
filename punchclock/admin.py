from django.contrib import admin
from punchclock.models import *
#from punchclock.models import ClockEvent.*



admin.site.register(Account)
admin.site.register(Department)
#admin.site.register(ClockEvent)


#this displays the CHANGE USER field for user. 
class UserAdmin(admin.ModelAdmin):
	fields = ['first_name', 'last_name', 'number', 'pay_rate', 'start_date', 'amount_paid', 'department', 'account' ]

admin.site.register(User, UserAdmin)


#class ClockEventAdmin(admin.ModelAdmin):
#	fields = ['user', 'department', 'ClockEvent.hours']
	
#admin.site.register(ClockEvent, ClockEventAdmin)
