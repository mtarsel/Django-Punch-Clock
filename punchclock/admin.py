from django.contrib import admin
from punchclock.models import *
from django.conf.urls import patterns, include, url
from django.http import *
from django.template.response import TemplateResponse


admin.site.register(Account)
admin.site.register(Department)

class UserAdmin(admin.ModelAdmin):
	fields = ['first_name', 'last_name', 'number', 'pay_rate', 'start_date', 'amount_paid', 'department', 'account', 'active' ]
		
	def get_urls(self):
		urls = super(UserAdmin, self).get_urls()
		my_urls = patterns('',
			(r'^generate_timecards/$', self.admin_site.admin_view(self.generate_timecards))
		)
		return my_urls + urls
		
	def generate_timecards( self, request, id ):
		if not request.user.is_authenticated():
			return HttpResponseRedirect('/admin/')
		timecards = [ ]
		#ids = request.POST[ 'ids' ]
		ids = request.POST.getlist('ids')
		for id in ids:
			user = User.objects.get( id=id )
			response = timecards( request, user )
			timecards.append( request.GETPDF_FROM_RESPONSE )
		return render_to_response( '/admin/generate_timecards.html' )	
		pass

	actions = [generate_timecards]

admin.site.register(User, UserAdmin)