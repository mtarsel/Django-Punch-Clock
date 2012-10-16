"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from punchclock.models import *


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
		
	
class Time(TestCase):
	event = models.ForeignKey(ClockEvent)
	def testTime(self):
		if self.in_time > self.out_time:
			return False
		return True