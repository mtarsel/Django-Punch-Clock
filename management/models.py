from django.db import models
from punchclock.models import UserAccount
from punchclock.models import Account

class UserAccountManagment(models.Model):
	user_account = models.ForeignKey(UserAccount)
	account_name = models.ForeignKey(Account)
	
#	def accountTotal(account_name, self):
		#generate total of account balances per year
		

class Reports(models.Model):
	spreadsheet = models.CharField(max_length=512)
	
	#def generateReports(self):
		

