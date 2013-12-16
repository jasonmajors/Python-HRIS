from django.db import models
from django.contrib.auth.models import User


class TimeOffRequest(models.Model):
	date_start = models.DateField(auto_now=False, auto_now_add=False)
	date_end = models.DateField(auto_now=False, auto_now_add=False)
	user = models.OneToOneField(User)
	status = models.CharField(max_length=25, default="PENDING")

	def __unicode__(self):
		return self.user

# Will build this out later. Adding an employee should create a "User".
# Think about how to combine the rango.views.register with creating an employee.
class Employee(models.Model):
	pass

# Will build this out later.
class Schedule(models.Model):
	#employee = models.ForeignKey(Employee)
	pass		
