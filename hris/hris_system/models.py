from django.db import models
from django.contrib.auth.models import User


class TimeOffRequest(models.Model):
	date_start = models.DateField(auto_now=False, auto_now_add=False)
	date_end = models.DateField(auto_now=False, auto_now_add=False)
	user = models.ForeignKey(User)
	status = models.CharField(max_length=25, default="PENDING")

	# many-to-one relationship between time off requests and employees
	# employee = models.ForiegnKey(Employee)
	def __unicode__(self):
		return self.user.username

# Will build this out later. Adding an employee should create a "User".
# See: https://docs.djangoproject.com/en/dev/topics/auth/default/#user-objects
class Employee(models.Model):
	pass

# Will build this out later.
class Schedule(models.Model):
	#employee = models.ForeignKey(Employee)
	pass		
