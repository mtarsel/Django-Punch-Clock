from django.contrib import admin
from punchclock.models import *

admin.site.register(Account)
admin.site.register(Department)

#this displays the CHANGE USER field for user. 
class UserAdmin(admin.ModelAdmin):
	fields = ['first_name', 'last_name', 'number', 'pay_rate', 'start_date', 'amount_paid', 'department', 'account' ]

admin.site.register(User, UserAdmin)

