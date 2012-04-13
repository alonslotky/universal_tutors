/*
 * In this file you find:
 *    questionPopup: throws an question and runs an url if you press confirm button
 *    windowPopup: loads a url in a iframe
 *    inputPopup: throws a box with and textarea and send text as data for an url (with django cookie)
 * 	  selectPopup: list of options to choose with different urls
 * 
 * by _nM_ (nelsonmonteiro.net) 
 * from rawjam.co.uk
 * 
 */
var infoPopup = $.Class.create({
	initialize: function (options) {
		this.title = options.title || '';
		this.text = options.text || '';
		this.prefix = options.prefix || '';
		
		this.width = options.width || 400;
		this.height = options.height || 'auto';
		
		this.fadeInOptions = options.fadeInOptions || {'duration': 250, 'queue': false};
		this.fadeOutOptions = options.fadeOutOptions || {'duration': 500, 'queue': false};
		
		var self = this;
		$(document.body).append(
			'<div id="'+self.prefix+'popup" class="popup hidden">'+
			'	<div id="'+self.prefix+'popup_window" class="popup_window">'+
			'		<div id="'+self.prefix+'popup_title" class="popup_window_title">'+ self.title +'<a id="'+self.prefix+'popup_close_window" href="javascript:;" class="popup_close_window">x</a></div>'+
			'		<div id="'+self.prefix+'popup_text" class="popup_question_container popup_window_container">'+ self.text +'</div>'+
			'		<div id="'+self.prefix+'popup_buttons" class="popup_buttons">'+
			'			<a href="javascript:;" id="'+self.prefix+'popup_button_confirm" class="popup_button_confirm">Close</a>'+
			'		</div>'+
			'	</div>'+
			'</div>'
		);

		$('#'+self.prefix+'popup').show();
		self.height = self.height=='auto'?$('#'+self.prefix+'popup_window').height():self.height;
		$('#'+self.prefix+'popup').hide();

	    $('#'+self.prefix+'popup_window').css({
	    	'width': self.width+'px',
	    	'top': (($(window).height() - self.height) / 2) + "px",
	    	'left': (($(window).width() - self.width) / 2) + "px"
	    });

		$('#'+self.prefix+'popup').fadeIn(500);
		$('#'+self.prefix+'popup_button_confirm').click(function(url){ self.close(); });
		$('#'+self.prefix+'popup_close_window').click(function(url){ self.close(); });
		
		$('#'+self.prefix+'popup_button_confirm').mouseover(function(url){ $(this).addClass('over', self.fadeInOptions); });
		$('#'+self.prefix+'popup_close_window').mouseover(function(url){ $(this).addClass('over', self.fadeInOptions); });

		$('#'+self.prefix+'popup_button_confirm').mouseout(function(url){ $(this).removeClass('over', self.fadeOutOptions); });
		$('#'+self.prefix+'popup_close_window').mouseout(function(url){ $(this).removeClass('over', self.fadeOutOptions); });

	},
	
	close: function() {
		var self = this;
		$('#'+self.prefix+'popup').fadeOut(250, function(){
			$('#'+self.prefix+'popup').remove();
		});
	}
});

var questionPopup = $.Class.create({
	initialize: function (options) {
		this.title = options.title || '';
		this.question = options.question || '';
		this.url = options.url || null;
		this.prefix = options.prefix || '';
		this.type = options.type || 'ajax';
		
		this.confirm_text = options.confirm_text || 'yes';
		this.cancel_text = options.cancel_text || 'no';
		
		this.width = options.width || 300;
		this.height = options.height || 'auto';
		
		this.beforeSend = options.beforeSend || null;
		this.complete = options.complete || null;
		
		this.fadeInOptions = options.fadeInOptions || {'duration': 250, 'queue': false};
		this.fadeOutOptions = options.fadeOutOptions || {'duration': 500, 'queue': false};
		
		this.type = (this.type == 'ajax' && !this.url && this.complete) ? 'action' : 'ajax';
		this.url = this.type == 'action' ? 'javascript:;' : this.url;
		
		var self = this;
		$(document.body).append(
			'<div id="'+self.prefix+'popup" class="popup hidden">'+
			'	<div id="'+self.prefix+'popup_window" class="popup_window">'+
			'		<div id="'+self.prefix+'popup_title" class="popup_window_title">'+ self.title +'<a id="'+self.prefix+'popup_close_window" href="javascript:;" class="popup_close_window">x</a></div>'+
			'		<div id="'+self.prefix+'popup_question" class="popup_question_container popup_window_container">'+ self.question +'</div>'+
			'		<div id="'+self.prefix+'popup_buttons" class="popup_buttons">'+
			'			<a href="javascript:;" id="'+self.prefix+'popup_button_confirm" class="popup_button_confirm">'+ self.confirm_text +'</a>'+
			'			<a href="javascript:;" id="'+self.prefix+'popup_button_cancel" class="popup_button_cancel">'+ self.cancel_text +'</a>'+
			'		</div>'+
			'	</div>'+
			'</div>'
		);

		$('#'+self.prefix+'popup').show();
		self.height = self.height=='auto'?$('#'+self.prefix+'popup_window').height():self.height;
		$('#'+self.prefix+'popup').hide();

	    $('#'+self.prefix+'popup_window').css({
	    	'width': self.width+'px',
	    	'top': (($(window).height() - self.height) / 2) + "px",
	    	'left': (($(window).width() - self.width) / 2) + "px"
	    });

		$('#'+self.prefix+'popup').fadeIn(500);
		$('#'+self.prefix+'popup_button_confirm').click(function(url){ self.close(self.url); });
		$('#'+self.prefix+'popup_close_window').click(function(url){ self.close(null); });
		$('#'+self.prefix+'popup_button_cancel').click(function(url){ self.close(null); });

		$('#'+self.prefix+'popup_button_confirm').mouseover(function(url){ $(this).addClass('over', self.fadeInOptions); });
		$('#'+self.prefix+'popup_button_cancel').mouseover(function(url){ $(this).addClass('over', self.fadeInOptions); });
		$('#'+self.prefix+'popup_close_window').mouseover(function(url){ $(this).addClass('over', self.fadeInOptions); });

		$('#'+self.prefix+'popup_button_confirm').mouseout(function(url){ $(this).removeClass('over', self.fadeOutOptions); });
		$('#'+self.prefix+'popup_button_cancel').mouseout(function(url){ $(this).removeClass('over', self.fadeOutOptions); });
		$('#'+self.prefix+'popup_close_window').mouseout(function(url){ $(this).removeClass('over', self.fadeOutOptions); });

	},
	
	close: function(url) {
		var self = this;
		$('#'+self.prefix+'popup').fadeOut(250, function(){
			$('#'+self.prefix+'popup').remove();
			if(url){
				if (self.type == 'action') { 
					if(self.complete)
						self.complete();
				} else { 
					if(self.type == 'window') {
						location.href = url;
					} else {
						$.ajax({
							url: url,
							beforeSend: function() {
								if(self.beforeSend)
									self.beforeSend();
							},
							complete: function() {
								if(self.complete)
									self.complete();
							}
						});					
					}
				}
			}
		});
	}
});


var windowPopup = $.Class.create({
	initialize: function (options) {
		this.title = options.title || '';
		this.url = options.url || null;
		this.prefix = options.prefix || '';
		
		this.extra_class = options.extra_class || '';
		
		this.width = options.width || 800;
		this.height = options.height || 500;
		
		this.onClose = options.onClose || null;
		
		this.fadeInOptions = options.fadeInOptions || {'duration': 250, 'queue': false};
		this.fadeOutOptions = options.fadeOutOptions || {'duration': 500, 'queue': false};
		
		var self = this;
		$(document.body).append(
			'<div id="'+self.prefix+'popup" class="popup hidden '+ self.window_extra_style +'">'+
			'	<div id="'+self.prefix+'popup_window" class="popup_window '+ self.window_extra_style +'">'+
			'		<div id="'+self.prefix+'popup_title" class="popup_window_title '+ self.window_extra_style +'">'+ self.title +'<a id="'+self.prefix+'popup_close_window" href="javascript:;" class="popup_close_window">x</a></div>'+
			'		<div id="'+self.prefix+'popup_content" class="popup_window_container '+ self.extra_class +'">'+
			' 			<iframe frameBorder="0" id="'+self.prefix+'popup_iframe" class="popup_iframe hidden '+ self.extra_class +'" />'+
			'			<div id="'+self.prefix+'popup_iframe_loading" class="popup_iframe_loading '+ self.extra_class +'"></div>'+
			'		</div>'+
			'	</div>'+
			'</div>'
		);

	    $('#'+self.prefix+'popup_window').css({
	    	'width': self.width+'px',
	    	'height': self.height+'px',
	    	'top': (($(window).height() - self.height) / 2) + "px",
	    	'left': (($(window).width() - self.width) / 2) + "px"
	    });

	    $('#'+self.prefix+'popup_content').css({
	    	'height': self.height - 66 + 'px'
	    });

		$('#'+self.prefix+'popup').fadeIn(500, function(){
			$('#'+self.prefix+'popup_iframe').attr('src', self.url);
		});
		$('#'+self.prefix+'popup_iframe').load(function(){ 
			$('#'+self.prefix+'popup_iframe_loading').fadeOut(function(){
				$('#'+self.prefix+'popup_iframe').fadeIn();			
			});
		});
		$('#'+self.prefix+'popup_close_window').click(function(url){ self.close(); });

		$('#'+self.prefix+'popup_close_window').mouseover(function(url){ $(this).addClass('over', self.fadeInOptions); });
		$('#'+self.prefix+'popup_close_window').mouseout(function(url){ $(this).removeClass('over', self.fadeOutOptions); });
	},
	
	loading: function() {
		var self = this;
		$('#'+self.prefix+'popup_iframe').hide();
		$('#'+self.prefix+'popup_iframe_loading').fadeIn();			
	},
	
	close: function() {
		var self = this;
		$('#'+self.prefix+'popup').fadeOut(250, function(){
			$('#'+self.prefix+'popup').remove();
			if(self.onClose){
				self.onClose();
			}
		});
	}
});


var inputPopup = $.Class.create({
	initialize: function (options) {
		this.title = options.title || '';
		this.text = options.text || '';
		this.url = options.url || null;
		this.method = options.method || 'post';
		this.prefix = options.prefix || '';
		
		this.confirm_text = options.confirm_text || 'send';
		this.cancel_text = options.cancel_text || 'cancel';
		
		this.width = options.width || 400;
		this.height = options.height || 300;
		
		this.beforeSend = options.beforeSend || null;
		this.complete = options.complete || null;
		
		this.formClass = options.formClass || 'uniForm';
		this.inputClass = options.inputClass || '';
		this.inputName = options.inputText || 'text';
		
		this.fadeInOptions = options.fadeInOptions || {'duration': 250, 'queue': false};
		this.fadeOutOptions = options.fadeOutOptions || {'duration': 500, 'queue': false};
		
		this.errorText = options.errorText || 'This field is required.';
		
		var self = this;
		$(document.body).append(
			'<div id="'+self.prefix+'popup" class="popup hidden">'+
			'	<div id="'+self.prefix+'popup_window" class="popup_window">'+
			'		<div id="'+self.prefix+'popup_title" class="popup_window_title">'+ self.title +'<a id="'+self.prefix+'popup_close_window" href="javascript:;" class="popup_close_window">x</a></div>'+
			'		<div id="'+self.prefix+'popup_content" class="popup_window_container">'+
			' 			<div id="'+self.prefix+'popup_text">'+ self.text +'</div>'+
			' 			<div id="'+self.prefix+'popup_error" style="display: none;">'+ self.errorText +'</div>'+
			' 			<div id="'+self.prefix+'popup_form_container">'+
			' 				<form id="'+self.prefix+'popup_form" class="'+ self.formClass +'">'+
			'					<textarea id="'+self.prefix+'popup_textarea" class="popup_input '+ self.inputClass +'" name="'+ self.inputName +'" />'+
			' 				</form>'+			
			' 			</div>'+			
			' 		</div>'+			
			'		<div id="'+self.prefix+'popup_buttons" class="popup_buttons">'+
			'			<a href="javascript:;" id="'+self.prefix+'popup_button_confirm" class="popup_button_confirm">'+ self.confirm_text +'</a>'+
			'			<a href="javascript:;" id="'+self.prefix+'popup_button_cancel" class="popup_button_cancel">'+ self.cancel_text +'</a>'+
			'		</div>'+
			'	</div>'+
			'</div>'
		);

		$('#'+self.prefix+'popup').show();
		self.height = self.height=='auto'?$('#'+self.prefix+'popup_window').height():self.height;
		$('#'+self.prefix+'popup').hide();

	    $('#'+self.prefix+'popup_window').css({
	    	'width': self.width+'px',
	    	'top': (($(window).height() - self.height) / 2) + "px",
	    	'left': (($(window).width() - self.width) / 2) + "px"
	    });

		$('#'+self.prefix+'popup').fadeIn(500);
		$('#'+self.prefix+'popup_button_confirm').click(function(url){ self.close(self.url); });
		$('#'+self.prefix+'popup_close_window').click(function(url){ self.close(null); });
		$('#'+self.prefix+'popup_button_cancel').click(function(url){ self.close(null); });

		$('#'+self.prefix+'popup_button_confirm').mouseover(function(url){ $(this).addClass('over', self.fadeInOptions); });
		$('#'+self.prefix+'popup_button_cancel').mouseover(function(url){ $(this).addClass('over', self.fadeInOptions); });
		$('#'+self.prefix+'popup_close_window').mouseover(function(url){ $(this).addClass('over', self.fadeInOptions); });

		$('#'+self.prefix+'popup_button_confirm').mouseout(function(url){ $(this).removeClass('over', self.fadeOutOptions); });
		$('#'+self.prefix+'popup_button_cancel').mouseout(function(url){ $(this).removeClass('over', self.fadeOutOptions); });
		$('#'+self.prefix+'popup_close_window').mouseout(function(url){ $(this).removeClass('over', self.fadeOutOptions); });

	},
	
	close: function(url) {
		var self = this;
		$('#'+self.prefix+'popup').fadeOut(250, function(){
			if(url){
				$.ajax({
					url: url,
					data: $('#'+self.prefix+'popup_form').serialize(),
					type: 'post',
				    beforeSend: function(xhr, settings){
				    	function getCookie(name) {
				    		var cookieValue = null;
							if (document.cookie && document.cookie != '') {
								var cookies = document.cookie.split(';');
								for (var i = 0; i < cookies.length; i++) {
									var cookie = jQuery.trim(cookies[i]);
									// Does this cookie string begin with the name we want?
									if (cookie.substring(0, name.length + 1) == (name + '=')) {
										cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
									}
								}
							}
							return cookieValue;
						}
						if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
							// Only send the token to relative URLs i.e. locally.
							xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
						}
						if(self.beforeSend)
						self.beforeSend();
					},
					complete: function() {
						$('#'+self.prefix+'popup').remove();
						if(self.complete)
							self.complete();
					}
				});
			}
		});
	}
});


var selectPopup = $.Class.create({
	/*
	 * HOW TO USE:
	 * 
	 * var my_var_name = new listPopup({
	 * 		'items': [ 
	 * 					{'category': 'Category name 1', 
	 * 				     'list': [ {'title': 'item1.1', 'url': 'link 1.1'}, {'title': 'item 1.2', 'url': 'link 1.2'} ]}
	 * 					{'category': null, 
	 * 				     'list': [ {'title': 'item 2.1', 'url': 'link 2.1'}, {'title': 'item 2.2', 'url': 'link 2.2'} ]}
	 * 				 ],
	 * 	    'title': 'My window title',
	 * 		'text': 'Choose one of bellow elements'
	 * });
	 * 
	 */ 
	
	
	initialize: function (options) {
		this.title = options.title || '';
		this.text = options.text || '';
		this.items = options.items || [];
		this.prefix = options.prefix || '';
				
		this.width = options.width || 350;
		this.height = options.height || 'auto';
		
		this.beforeSend = options.beforeSend || null;
		this.complete = options.complete || null;
		
		this.confirmation = options.confirmation || false;
		this.confirmation_title = options.confirmation_title || this.text;
		this.confirmation_question = options.confirmation_question || 'Confirm option';
		
		this.fadeInOptions = options.fadeInOptions || {'duration': 250, 'queue': false};
		this.fadeOutOptions = options.fadeOutOptions || {'duration': 500, 'queue': false};
		var self = this;
		$(document.body).append(
			'<div id="'+self.prefix+'popup" class="popup hidden">'+
			'	<div id="'+self.prefix+'popup_window" class="popup_window">'+
			'		<div id="'+self.prefix+'popup_title" class="popup_window_title">'+ self.title +'<a id="'+self.prefix+'popup_close_window" href="javascript:;" class="popup_close_window">x</a></div>'+
			'		<div id="'+self.prefix+'popup_container" class="popup_window_container">'+ self.text +'</div>'+
			'		<div id="'+self.prefix+'popup_buttons" class="popup_buttons">'+
			'			<a href="javascript:;" id="'+self.prefix+'popup_button_cancel" class="popup_button_cancel">Cancel</a>'+
			'		</div>'+
			'	</div>'+
			'</div>'
		);

		var elements = '';

		for (i=0; i < self.items.length; i++){
			var category = self.items[i].category;
			var list = self.items[i].list;
			
			elements += '<div class="popup_list_category_container">';
			
			if(category)
				elements += '<div class="popup_list_category_title">'+category+'</div>';
			
			for (j=0; j < list.length; j++) {	
				var title = list[j].title;
				var url = list[j].url;
				
				elements += '<div class="popup_list_item_container"><a id="'+self.prefix+i+'-'+j+'popup_list_item" class="popup_list_item" href="'+ url +'">'+title+'</a></div>';
			}
			
			elements += '<p>&nbsp;</p></div>';
		}
		$('#'+self.prefix+'popup_container').append(elements);
	
		$('#'+self.prefix+'popup').show();
		self.height = self.height=='auto'?$('#'+self.prefix+'popup_window').height():self.height;
		$('#'+self.prefix+'popup').hide();

	    $('#'+self.prefix+'popup_window').css({
	    	'width': self.width+'px',
	    	'top': (($(window).height() - self.height) / 2) + "px",
	    	'left': (($(window).width() - self.width) / 2) + "px"
	    });

		$('#'+self.prefix+'popup').fadeIn(500);
		$('#'+self.prefix+'popup_close_window').click(function(url){ self.close(null); });
		$('#'+self.prefix+'popup_button_cancel').click(function(url){ self.close(null); });
		$('.popup_list_item_container').mouseover(function(url){ $(this).addClass('over', self.fadeInOptions); });
		$('.popup_list_item_container').mouseout(function(url){ $(this).removeClass('over', self.fadeOutOptions); });
		$('.popup_list_item').click(function(e){ e.preventDefault(); });  
		$('.popup_list_item_container').click(function(e){ 
			e.preventDefault();  
			var url = $('.popup_list_item',this).attr('href');
			var title = $('.popup_list_item',this).html();
			
			if (self.confirmation) {
				new questionPopup({
					'url': 	url,
					'title': self.confirmation_title,
					'question': self.confirmation_question +" '"+ title +"'?",
					'beforeSend': function() {
						if(self.beforeSend)
							self.beforeSend();
					},
					'complete': function(){
						self.close(null);
						if(self.complete)
							self.complete();
					}
				});					
			} else {
				self.close(url);
			}
		});

	},
	
	close: function(url) {
		var self = this;
		$('#'+self.prefix+'popup').fadeOut(250, function(){
			$('#'+self.prefix+'popup').remove();
			if(url){
				$.ajax({
					url: url,
					beforeSend: function() {
						if(self.beforeSend)
							self.beforeSend();
					},
					complete: function() {
						if(self.complete)
							self.complete();
					}
				});
			}
		});
	}
});


var progressBarPopup = $.Class.create({
	/* 
	 * Create a popup progress bar
	 * needs jquery.progressbar
	 * 
	 */
	
	initialize: function (options) {
		this.title = options.title || '';
		this.url = options.url || null;
		this.form = options.form || '';
		this.prefix = options.prefix || '';
		this.type = options.type || 'nginx'; /* nginx or django */
		
		this.progress_var = options.progress_var || 'X-Progress-ID';
		this.progress_id = options.progress_id || '';
		
		this.width = options.width || 300;
		this.height = options.height || 'auto';
		
		this.complete = options.complete || null;
		this.checkBefore = options.checkBefore || null;
		
		this.fadeInOptions = options.fadeInOptions || {'duration': 250, 'queue': false};
		this.fadeOutOptions = options.fadeOutOptions || {'duration': 500, 'queue': false};
		
		this.progressBarPopupPath = options.progressBarPopupPath || globalProgressBarPopupPath || '/static/js/lib/popup/popup.js';
		this.jqueryPath = options.jqueryPath || globaljQueryPath || '/static/js/lib/jquery-1.6.4.min.js';
		this.jqueryClassPath = options.jqueryClassPath || globaljQueryClassPath || '/static/js/lib/jquery.class.js';
		var self = this;
		
		$(document.body).append('<img src="'+ MEDIA_URL +'js/lib/popup/ajax-loader.gif" class="hidden" />');
		
		$('form'+ self.form).submit(function(e){
			if(self.checkBefore && !self.checkBefore()) {
				e.preventDefault();
				return false;
			}

			$(document.body).append(
				'<div id="'+self.prefix+'popup" class="popup hidden">'+
				'	<div id="'+self.prefix+'popup_window" class="popup_window">'+
				'		<div id="'+self.prefix+'popup_title" class="popup_window_title">Uploading | Please wait</div>'+
				'		<div class="popup_window_container">'+
				'			<div id="'+self.prefix+'popup_progress_loading" class="popup_progress_loading">'+
			    '				<img src="'+ MEDIA_URL +'js/lib/popup/ajax-loader.gif" />'+
			    '			</div>'+
			    '		</div>'+
				'	</div>'+
				'</div>'
			);

			$('#'+self.prefix+'popup').show();
			self.height = self.height=='auto'?$('#'+self.prefix+'popup_window').height():self.height;
			$('#'+self.prefix+'popup').hide();
	
		    $('#'+self.prefix+'popup_window').css({
		    	'width': self.width+'px',
		    	'top': (($(window).height() - self.height) / 2) + "px",
		    	'left': (($(window).width() - self.width) / 2) + "px"
		    });
	
			$('#'+self.prefix+'popup').fadeIn(500);
			
			
			/* REAL PROGRESS BAR CODE... SOME BUGS IN SAFARI AND CHROME 

			var url = $('form'+ self.form).attr('action') || '';
			url += '?'+ self.progress_var +'='+ self.progress_id;
			
			$('form'+ self.form).attr('action', url);

			$(document.body).append(
				'<div id="'+self.prefix+'popup" class="popup hidden">'+
				'	<div id="'+self.prefix+'popup_window" class="popup_window">'+
				'		<div id="'+self.prefix+'popup_title" class="popup_window_title">'+ self.title +'</div>'+
				'		<div class="popup_window_container">'+
				'			<div id="'+self.prefix+'popup_progress_bar_container" class="popup_progress_bar_container">'+
			    '				<div id="'+self.prefix+'popup_progress_bar" class="popup_progress_bar"></div>'+
			    '				<div id="'+self.prefix+'popup_progress_bar_text" class="popup_progress_bar_text">0%</div>'+
			    '			</div>'+
			    '		</div>'+
				'	</div>'+
				'</div>'
			);
	
			$('#'+self.prefix+'popup').show();
			self.height = self.height=='auto'?$('#'+self.prefix+'popup_window').height():self.height;
			$('#'+self.prefix+'popup').hide();
	
		    $('#'+self.prefix+'popup_window').css({
		    	'width': self.width+'px',
		    	'top': (($(window).height() - self.height) / 2) + "px",
		    	'left': (($(window).width() - self.width) / 2) + "px"
		    });
	
			$('#'+self.prefix+'popup').fadeIn(500);

		
		    if($.browser.webkit) {
		    	iframe = document.createElement('iframe');
		    	iframe.name = 'progressFrame';
		    	$(iframe).css({width: '0', height: '0', position: 'absolute', top: '-3000px'});
		    	document.body.appendChild(iframe);
		      
		      	var d = iframe.contentWindow.document;
		      	d.open();
		      	d.write('<html>'+
		      			'   <head>'+
		      			'      <scr' + 'ipt type="text\/javascript" src="'+self.jqueryPath+'"><\/scr' + 'ipt>'+
		      			'      <scr' + 'ipt type="text\/javascript" src="'+self.jqueryClassPath+'"><\/scr' + 'ipt>'+
		      			'      <scr' + 'ipt type="text\/javascript" src="'+self.progressBarPopupPath+'"><\/scr' + 'ipt>'+
		      			'      <scr' + 'ipt type="text\/javascript">jQuery.uploadProgressBarPopup("'+self.prefix+'", "'+self.url+'?'+self.progress_var+'='+self.progress_id+'");<\/scr' + 'ipt>'+
		      			'   </head>'+
		      			'   <body>'+
		      			'   </body>'+
		      			'</html>');
		      	d.close();
		    } else {
				jQuery.uploadProgressBarPopup(self.prefix, self.url+'?'+self.progress_var+'='+self.progress_id);
		    }
		    
		    */
		});

	}
});

(function($) {
	jQuery.uploadProgressBarPopup = function(prefix, url) {
	  	text = $.browser.webkit ? $('#'+ prefix +'popup_progress_bar_text', parent.document) : $('#'+ prefix +'popup_progress_bar_text');
	  	bar = $.browser.webkit ? $('#'+ prefix +'popup_progress_bar', parent.document) : $('#'+ prefix +'popup_progress_bar');
	  	
	  	setTimeout(function(){ 
		  	$.ajax({
			    type: 'get',
			    url: url,
			    success: function(result) {
					data = eval(result);
					if (data == null) {
						text.html('0%');
						bar.css('width','0%');
					} else {
						var percentage = Math.floor(100 * parseInt(data.received) / parseInt(data.size));
						if (percentage > 0) {
							text.html(percentage + '%');
							bar.css('width', percentage + '%');
						}
					}
					if (result.state != 'done' && result.state != 'error') {
				  		jQuery.uploadProgressBarPopup(prefix, url);
			  		}
			  	},
			  	error: function(jqXHR, textStatus, errorThrown) {
			  		jQuery.uploadProgressBarPopup(prefix, url);
			  	}
		  	});
	  	}, 3000);
	};
})(jQuery);