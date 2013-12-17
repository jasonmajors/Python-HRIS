from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from hris_system.forms import TimeOffRequestForm, EmployeeForm
from hris_system.models import TimeOffRequest 

def index(request):
	context = RequestContext(request)
	context_dict = {}

	return render_to_response('hris_system/index.html', context_dict, context)

@login_required
def submit(request):
	context = RequestContext(request)
	context_dict = {}

	if request.method == 'POST':
		form = TimeOffRequestForm(request.POST)

		if form.is_valid():
			time_off_request = form.save(commit=False)

			user = User.objects.get(username=request.user)
			time_off_request.user = user
			time_off_request.save()

			return index(request)
		else:
			print form.errors
	else:
		form = TimeOffRequestForm()

	return render_to_response('hris_system/submit.html', {'form':form}, context)				

def user_login(request):
	context = RequestContext(request)
	failed_attempt = False

	if request.method == 'POST':
		# Information from the login form.
		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(username=username, password=password)

		if user is not None:
			if user.is_active:
				login(request, user)

				return HttpResponseRedirect('/hris/')

			else:
				disabled = True

				return render_to_response("hris_system/login.html", {"disabled": disabled}, context)	
		else:
			failed_attempt = True

			print "Invalid login: {0}, {1}".format(username, password)

			return render_to_response("hris_system/login.html", {"failed_attempt": failed_attempt}, context)

	else:
		return render_to_response('hris_system/login.html', {}, context)				

@login_required
def user_logout(request):
	logout(request)

	return HttpResponseRedirect('/hris/')

@login_required
def get_timeoff_requests(request):
	context = RequestContext(request)
	context_dict = {}

	pending_requests = TimeOffRequest.objects.filter(status="PENDING")
	approved_requests = TimeOffRequest.objects.filter(status="APPROVED")
	denied_requests = TimeOffRequest.objects.filter(status="DENIED")

	context_dict['pending_requests'] = pending_requests
	context_dict['approved_requests'] = approved_requests
	context_dict['denied_requests'] = denied_requests

	return render_to_response('hris_system/timeoff.html', context_dict, context)

@login_required
def add_employee(request):
	context = RequestContext(request)
	context_dict = {}

	if request.method == "POST":
		form = EmployeeForm(request.POST)

		if form.is_valid():
			
			employee = form.save(commit=False)
			username = employee.first_name + "_" + employee.last_name
			new_user = User.objects.create_user(username=username, password="password")
			employee.user = new_user
			employee.save()

			return index(request)
		else:
			print form.errors
	else:
		form = EmployeeForm()

	return render_to_response('hris_system/add_employee.html', {'form':form}, context)
