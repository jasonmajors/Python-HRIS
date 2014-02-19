from django.conf.urls import patterns, url
from hris_system import views

urlpatterns = patterns('',
		url(r'^$', views.index, name='index'),
		url(r'^submit/$', views.submit_timeoff, name='submit_timeoff'),
		url(r'^timeoff/(?P<request_status>\w+)/$', views.get_timeoff_requests, name='requests'),
		url(r'^handle_timeoff/(?P<request_id>\w+)/(?P<approve_or_deny>\w+)/$', views.handle_timeoff, name="handle_timeoff"),
		url(r'^login/$', views.user_login, name='login'),
		url(r'^logout/$', views.user_logout, name='logout'),
		url(r'^add_employee/$', views.add_employee, name='add_employee'),
		url(r'^suggest_employee/$', views.suggest_employee, name='suggest_employee'),
		url(r'^employee/(?P<employee_url>\w+)/$', views.get_employee_page, name='get_employee_page'),
		url(r'^employee/(?P<employee_url>\w+)/edit/$', views.edit_employee_page, name='edit_employee_page'),
		url(r'^employee/(?P<employee_url>\w+)/schedule/edit/$', views.edit_employee_schedule, name='edit_employee_schedule'),
		url(r'^my_requests/$', views.my_timeoff_requests, name='my_timeoff_requests'),
		url(r'^update_password/$', views.update_password, name='update_password'),
		url(r'^cancel_request/(?P<request_id>\w+)/$', views.cancel_request, name='cancel_request'),

		)