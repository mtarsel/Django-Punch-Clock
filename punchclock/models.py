from django.db import models
from datetime import datetime
from django.utils import timezone

class Account(models.Model):
	name = models.CharField(max_length=512)
	number = models.CharField(max_length=512)
	priority = models.IntegerField()
	
	def __unicode__(self):
		return unicode(self.name)
		
class Department(models.Model):
	name = models.CharField(max_length=512)
	
	def __unicode__(self):
		return unicode(self.name)

class User(models.Model):
	number = models.IntegerField()
	first_name = models.CharField(max_length=512)
	last_name = models.CharField(max_length=512)
	pay_rate = models.FloatField()
	start_date = models.DateField()
	amount_paid = models.FloatField()
	department = models.ForeignKey(Department)
	account = models.ForeignKey(Account)
	
	def __unicode__(self):
		return unicode(self.last_name) + ', ' + unicode(self.first_name) + ':' + unicode(self.number) + ' $' + unicode(self.pay_rate)
	

class UserAccount(models.Model):
	user = models.ForeignKey(User)
	account = models.ForeignKey(Account)
	start_date = models.DateField()
	end_date = models.DateField()
	amount = models.FloatField()
	priority = models.IntegerField()
	
	def __unicode__(self):
		return unicode(self.user)

	
class ClockEvent(models.Model):
	user = models.ForeignKey(User)
	department = models.ForeignKey(Department)
	account = models.ForeignKey(Account)
	in_time = models.DateTimeField()
	out_time = models.DateTimeField()
	pay_rate = models.FloatField()
	
	def clockIn(self, user, department):
		
		if not self.in_time == None:
			return
		
		self.pay_rate = user.pay_rate
		self.department = department
		self.user = user
		#self.in_time = datetime.now()
		self.in_time = timezone.now()
		self.save()
		return
		
	def clockOut(self):
		
		if not self.out_time == None and not self.in_time == None:
			return
			
		self.pay_rate = user.pay_rate
		#self.out_time = datetime.now()
		self.out_time = timezone.now()
		self.save()
		return
		
	def testTime(self):
		if self.in_time > self.out_time:
			return False
		return True
		#make sure in time and out time are defined
		
	def hours(account, self):
		td = self.out_time - self.in_time
		return float(td.total_seconds()/3600)	
		
	def amount_payed(self):
		return self.pay_rate * self.hours()
	
	def account_manage(amount_payed, account, self):
		self.account = account
		self.amount_payed = amount_payed
		return self.amount_payed - self.account
		
	
	def __unicode__(self):
		return unicode(self.last_name) + ', ' + unicode(self.first_name) + ':' + unicode(self.number)