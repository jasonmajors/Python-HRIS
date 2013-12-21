from django.db import models
from django.contrib.auth.models import User


# Will build this out later. Adding an employee should create a "User".
# See: https://docs.djangoproject.com/en/dev/topics/auth/default/#user-objects
class Employee(models.Model):
	user = models.OneToOneField(User)
	last_name = models.CharField(max_length=25)
	first_name = models.CharField(max_length=25)

	def __unicode__(self):
		return self.user.username

class TimeOffRequest(models.Model):
	employee = models.ForeignKey(Employee)
	date_start = models.DateField(auto_now=False, auto_now_add=False)
	date_end = models.DateField(auto_now=False, auto_now_add=False)
	status = models.CharField(max_length=25, default="PENDING")

	def __unicode__(self):
		return self.employee.user.username

# Will build this out later.
class Schedule(models.Model):
	#employee = models.ForeignKey(Employee)
	pass		
