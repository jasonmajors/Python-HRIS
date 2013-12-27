from django import forms
from django.contrib.auth.models import User
from hris_system.models import TimeOffRequest, Employee

class TimeOffRequestForm(forms.ModelForm):
	date_start = forms.DateField(help_text="Please enter the beginning date of your time off request (mm/dd/yyyy).")
	date_end = forms.DateField(help_text="Please enter the final day of your request (mm/dd/yyyy).")
	status = forms.CharField(widget=forms.HiddenInput(), max_length=25, initial="PENDING")
	
	class Meta:
		model = TimeOffRequest
		fields = ('date_start', 'date_end', 'status')

class EmployeeForm(forms.ModelForm):		
	last_name = forms.CharField(max_length=25, help_text="Employee's LAST NAME")
	first_name = forms.CharField(max_length=25, help_text="Employee's FIRST NAME")
	position = forms.CharField(max_length=25, help_text="Employee's POSITION")
	#department = forms.ChoiceField()
	hire_date = forms.DateField(help_text="Employee's hire date")
	phone_number = forms.CharField(max_length=15, help_text="Phone number")
	address = forms.CharField(max_length=25, help_text="Street address")
	city = forms.CharField(max_length=25, help_text="City")
	state = forms.CharField(max_length=2, help_text="State")
	zipcode = forms.IntegerField(help_text="Zipcode")

	class Meta:
		model = Employee
		fields = ('last_name', 
				'first_name', 
				'position',
				#'department', 
				'hire_date', 
				'phone_number',
				'address',
				'city',
				'state',
				'zipcode'
				)