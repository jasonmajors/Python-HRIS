$(document).ready(function() {
	
	$('.approve').click(function(){
		var reqid = $(this).attr("data-reqid");
		var approvedeny = $(this).attr("data-approvedeny");
		var me = $(this);
		$.get('/hris/handle_timeoff/', {request_id: reqid, approve_or_deny: approvedeny}, function(data){
			$('#requests').html(data);
			me.hide();
		});
	});

	$('.deny').click(function(){
		var reqid = $(this).attr("data-reqid");
		var approvedeny = $(this).attr("data-approvedeny");
		var me = $(this);
		$.get('/hris/handle_timeoff/', {request_id: reqid, approve_or_deny: approvedeny}, function(data){
			$('#requests').html(data);
			me.hide();
		});
	});

	$("#suggestion").keyup(function(){
		var query = $(this).val();
		$.get('/hris/suggest_employee/', {suggestion: query}, function(data){
			$('#emps').html(data);
		});
	});
});