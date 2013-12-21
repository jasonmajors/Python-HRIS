from django.conf.urls import patterns, url
from hris_system import views

urlpatterns = patterns('',
		url(r'^$', views.index, name='index'),
		url(r'^submit/$', views.submit, name='submit'),
		url(r'^timeoff/(?P<request_status>\w+)/$', views.get_timeoff_requests, name='requests'),
		url(r'^approve_timeoff/$', views.approve_timeoff, name="approve_timeoff"),
		url(r'^login/$', views.user_login, name='login'),
		url(r'^logout/$', views.user_logout, name='logout'),
		url(r'^add_employee/$', views.add_employee, name='add_employee'),
		url(r'^suggest_employee/$', views.suggest_employee, name='suggest_employee'),

		)