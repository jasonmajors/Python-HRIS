$(document).ready(function() {
	
	$("#suggestion").keyup(function(){
		var query = $(this).val();
		$.get('/hris/suggest_employee/', {suggestion: query}, function(data){
			$('#emps').html(data);
		});
	});
});