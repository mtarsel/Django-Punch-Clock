from django.db import models
from datetime import datetime
from django.utils import timezone
from django.contrib import admin
from django.conf.urls import patterns, include, url
from django.forms import ModelForm
from django.http import Http404

class Account(models.Model):
	name = models.CharField(max_length=512)
	number = models.CharField(max_length=512)
	priority = models.IntegerField()
	total = models.IntegerField()		
	
	def __unicode__(self):
		return unicode(self.name)
		
class Department(models.Model):
	name = models.CharField(max_length=512)
	#students can have 2 departments with same payrate
	
	def __unicode__(self):
		return unicode(self.name)

class User(models.Model):
	number = models.IntegerField(max_length=8)
	first_name = models.CharField(max_length=512)
	last_name = models.CharField(max_length=512)
	pay_rate = models.FloatField()
	start_date = models.DateField()
	amount_paid = models.FloatField()
	department = models.ForeignKey(Department)#user can have multiple departments
	account = models.ForeignKey(Account)#can have multiple accounts
	
	#if they work for one year, increase pay by $0.25
	
	def __unicode__(self):
		return unicode(self.last_name) + ', ' + unicode(self.first_name) + ':' + unicode(self.number) + ' $' + unicode(self.pay_rate)

class ClockEvent(models.Model):
	user = models.ForeignKey(User)
	department = models.ForeignKey(Department)
	account = models.ForeignKey(Account, null=True, blank=True)
	in_time = models.DateTimeField( null=True, blank=True )
	out_time = models.DateTimeField( null=True, blank=True )
	pay_rate = models.FloatField()
	
	def clockIn(self, user, department):
		
		if not self.in_time == None:
			return

		self.pay_rate = user.pay_rate
		self.department = department
		self.user = user
		self.in_time = timezone.now()
		self.save()
		return
		
	def clockOut(self, user, department):
		
		if not self.out_time == None and not self.in_time == None:
			print 'Error!'#debug
			return
		self.user = user
		self.pay_rate = user.pay_rate
		self.department = department
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

# choices
DEPARTMENT_CHOICES = (
    ( 'Web Design', 'Web Design' ),
    ( 'Front Desk', 'Front Desk' ),
)

class Index( models.Model ):
    student_number = models.IntegerField( max_length=8 )
    department = models.CharField( max_length=40, choices=DEPARTMENT_CHOICES )

class IndexForm( ModelForm ):
	class Meta:
		model = Index
