from django.db import models
from punchclock.models import UserAccount
from punchclock.models import Account
from punchclock.models import Department


class UserAccountManagement(models.Model):
	user_account = models.ForeignKey(UserAccount)
	account_name = models.ForeignKey(Account)
	department_name = models.ForeignKey(Department)
		
	#def __unicode__(self):
		#return unicode(self.user_account) + ', ' + unicode(self.account_name) + ', ' + unicode(self.department_name)

#	def accountTotal(account_name, self):
		#generate total of account balances per year
		

class Reports(models.Model):
	spreadsheet = models.CharField(max_length=512)
	
	#def generateReports(self):
		

