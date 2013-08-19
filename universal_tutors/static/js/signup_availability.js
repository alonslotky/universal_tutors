var schedule_period_id;
var schedule_period_move_left;
var schedule_period_move_right;
var schedule_period_left_position;
var schedule_period_width;
var schedule_period_x;
var schedule_calendar_day_id;
var schedule_calendar_day_left_position;
var schedule_calendar_day_width;
var schedule_calendar_day_x;


var availability_periods = {}

$('.new-schedule-period').live('mousedown', function(e){
	e.preventDefault();
	schedule_period_id = $(this).attr('id');
});

$('.new-schedule-period .left').live('mousedown', function(e){
	e.preventDefault();
	schedule_period_id = $(this).parent().attr('id');
	schedule_period_move_left = true;
	schedule_period_left_position = $('#' + schedule_period_id).position().left;
	schedule_period_width = $('#' + schedule_period_id).width();
	schedule_period_x = e.pageX;
});

$('.new-schedule-period .right').live('mousedown', function(e){
	e.preventDefault();
	schedule_period_id = $(this).parent().attr('id');
	schedule_period_move_right = true;
	schedule_period_left_position = $('#' + schedule_period_id).position().left;
	schedule_period_width = $('#' + schedule_period_id).width();
	schedule_period_x = e.pageX;
});

$('.new-schedule-calendar-day').live('mousedown', function(e){
	e.preventDefault();
	schedule_calendar_day_id = $(this).attr('id');
	schedule_calendar_day_x = e.pageX;
	schedule_calendar_day_left_position = e.pageX - $(this).offset().left;
	schedule_calendar_day_width = 0;
});

$('.new-schedule-period .options').live('click', function(e){
	if($(this).hasClass('open')) {
		$('.options-container', $(this)).addClass('hidden');
		$(this).removeClass('open');
	} else {
		$('.options-container', $(this)).removeClass('hidden');
		$(this).addClass('open');
	}
});

$('.new-schedule-delete-period').live('click', function(){
	var parent = $(this).parent();
	while (!parent.hasClass('new-schedule-period')) {
		parent = parent.parent();
	}
	
	var id = parent.attr('id').split('_')[1];
	delete availability_periods[id]
	parent.fadeOut(function(){
		$(this).remove();
		$.get(DELETE_WEEK_PERIOD_URL+ id +'/');
	});
});


$(window).mousemove(function(e) {
	if(schedule_period_id && (schedule_period_move_left || schedule_period_move_right)) {
		e.preventDefault();
		var left;
		var width;
		var fullwidth = parseFloat($('#' + schedule_period_id).parent().width());	
		
		if(schedule_period_move_left) {
			left = Math.round((schedule_period_left_position + (e.pageX - schedule_period_x)) / fullwidth * 100);
			width = Math.round((schedule_period_width - (e.pageX - schedule_period_x)) / fullwidth * 100);
		}
		
		if(schedule_period_move_right) {
			left = Math.round(schedule_period_left_position / fullwidth * 100);
			width = Math.round((schedule_period_width + (e.pageX - schedule_period_x)) / fullwidth * 100);
		}
		
		if(isPeriodValid(left, width, fullwidth)) {
			$('#' + schedule_period_id).css({
				'left': left+'%',
				'width': width+'%'
			});			
		}

	} else if(schedule_calendar_day_id && !(schedule_period_id)) {
		
		var fullwidth = parseFloat($('#' + schedule_calendar_day_id).width());
		var left = Math.round(schedule_calendar_day_left_position / fullwidth * 100);
		var width = Math.round((e.pageX - schedule_calendar_day_x) / fullwidth * 100);
		
		
		if(isPeriodValid(left, width, fullwidth)) {
			$('#'+ schedule_calendar_day_id).append(
				'<div id="schedule-period_0" class="new-schedule-period" style="left:'+ left +'%;width:'+ width +'%;">'+
				'	<div class="left">&laquo;</div>'+
				'	<div class="right">&raquo;</div>'+
				'</div>'
			);
			
			schedule_calendar_day_id = null;
			schedule_period_id = 'schedule-period_0';
			schedule_period_move_right = true;
			schedule_period_left_position = schedule_calendar_day_left_position;
			schedule_period_width = schedule_calendar_day_width;
			schedule_period_x = e.pageX;
		}		
	}
});

$(window).mouseup(function() {
	if (schedule_period_id && (schedule_period_move_left || schedule_period_move_right)) {
		var id = parseInt(schedule_period_id.split('_')[1]);
		var el = $('#'+schedule_period_id);
		var weekday = el.parent().attr('id').split('_')[1];

		var fullwidth = parseFloat(el.parent().width());	
		var left = Math.round(el.position().left / fullwidth * 100) - 4;
		var right = Math.round(left + el.outerWidth() / fullwidth * 100);
		
		var begin_hour = parseInt(left / 4);
		var begin_minute = parseInt((left % 4) * 15);
		var end_hour = parseInt(right / 4);
		var end_minute = parseInt((right % 4) * 15);
		end_hour = end_hour!=24 ? end_hour : 0;
		
		begin = begin_hour +'-'+ begin_minute;
		end = end_hour +'-'+ end_minute;
		
		if (id!=0){
			availability_periods[id] = {'weekday': weekday, 'begin_hour': begin_hour, 'begin_minute': begin_minute, 'end_hour': end_hour, 'end_minute': end_minute}
		}
		//period = {'weekday': weekday, 'begin_hour': begin_hour, 'begin_minute': begin_minute, 'end_hour': end_hour, 'end_minute': end_minute};
		if(id) {
			$.get(EDIT_WEEK_PERIOD_URL+ id +'/'+ begin +'/'+ end +'/'+ weekday +'/');
		} else {
			$.ajax({
				url: EDIT_WEEK_PERIOD_URL+ id +'/'+ begin +'/'+ end +'/'+ weekday +'/',
				type: 'GET',
				error: function() { el.remove(); },
				success: function(data) {
					var id = data.split('_')[1].split('"')[0];
					availability_periods[id] = {'weekday': weekday, 'begin_hour': begin_hour, 'begin_minute': begin_minute, 'end_hour': end_hour, 'end_minute': end_minute}
					$(data).insertBefore(el);
					el.remove();
					$('input[name=availability]').val(JSON.stringify(availability_periods));
					
				}
			});
		}
	}
	schedule_period_id = null;
	schedule_period_move_left = false;
	schedule_period_move_right = false;
	schedule_calendar_day_id = null;
});


function isPeriodValid(left, width, fullwidth) {
	var right = left + width;
	if(width>=2 && left>=4 && right<=100) {
		var schedule_day = schedule_period_id ? $('#'+schedule_period_id).parent() : $('#'+ schedule_calendar_day_id);
		
		var return_value = true;
		$('.new-schedule-period', schedule_day).each(function(){
			if($(this).attr('id') != schedule_period_id) {
				this_left = $(this).position().left / fullwidth * 100
				this_right = this_left + $(this).width() / fullwidth * 100;
				
				if( (left < this_left && this_left < right) || (left < this_right && this_right < right) 
				     || (this_left < left && left < this_right) || (this_left < right && right < this_right) ) {
					return_value = false;
				}
			}				
		});
		
		return return_value;
	}

	return false;
}

 function showModal1() {
			         $('#modal-add-availability').foundation('reveal', 'open'); 
			         $('#modal-add-availability').foundation('reveal', 'close');}
/*
$('#student-signup-form').on('submit',function(e){
	e.preventDefault();
	var formData = $('#student-signup-form').serializeArray();
	formData.push({ name: "availability", value: JSON.stringify(availability_periods)});
	
	$('#student-signup-form').submit(function() { // catch the form's submit event
            $.ajax({ // create an AJAX call...
                data: formData, // get the form data
                type: 'POST', // GET or POST
                url: TUTOR_SIGNUP_URL // the file to call
                
              });
            
            
 });

});
*/
