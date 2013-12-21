$(document).ready(function() {
	// Not currently working.
	$('.approve').click(function(){
		var reqid = $(this).attr("data-reqid");
		var me = $(this)
		$.get('/hris/approve_timeoff/', {request_id: reqid}, function(data){
			//$('#requests').html(data);
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