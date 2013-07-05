if (!Array.indexOf) {
  Array.prototype.indexOf = function (obj, start) {
    for (var i = (start || 0); i < this.length; i++) {
      if (this[i] == obj) {
        return i;
      }
    }
    return -1;
  }
}

var AutoComplete = $.Class.create({
	/**
	 * Class to handle Tabs on the site
	 */
	
	initialize: function(options) {
		this.inputId = options.inputId || '#id-item-input';
		this.formId = options.formId || '#items-form';
		this.errorCls = options.errorCls || '#item-add-error';
		
		this.id = options.id || '';
		this.main_container = options.main_container || '#items-main-container';
		this.list_container = options.list_container || '#items-container';
		this.item_container = options.item_container || 'ac_item-container';
		this.id_items = options.id_items || '#id_item';
		this.id_new_items = options.id_new_items || '#id_new_items';
		this.text = options.text || 'ac_item-text';
		this.del = options.del || 'ac_item-delete';
		this.prefix = options.prefix || 'related-item';
		this.max = options.max || 0;
		
		this.no_new_items = 0;
		
		this.add_new_items = options.add_new_items || false;
		
		this.AUTOCOMPLETE_URL = options.url || '';
		
		this.tracked_items = new Array();
		this.tracked_new_items = new Array();

		var inputId = this.inputId;
		var formId = this.formId
		var errorCls = this.errorCls;
		var add_error = false;
		var tracked_items = this.tracked_items;
		var tracked_new_items = this.tracked_new_items;
		var main_container = this.main_container;
		var self = this;
		var add_new_items = this.add_new_items;
		var AUTOCOMPLETE_URL = this.AUTOCOMPLETE_URL;
		var id_items = this.id_items;
		var id_new_items = this.id_new_items;
		
		$(document).ready(function(){ 
			// handle autocomplete data
			$(inputId).autocomplete(AUTOCOMPLETE_URL, {
				extraParams: {
					'q': function(){
						return $(inputId).val();
					}
				},
				formatItem: function(r){
					return r[1];
				},
				parse: function(r){
					var rvData = eval(r);
					var rv = [];
					$.each(rvData, function(index, row){
						rv.push({
							data: row,
							value: row[1],
							result: row[1]
						});
					});
					return rv;
				}	
			}).bind("result", function(data, value){
				// TODO: load info about item via AJAX
				var itemId = value[0];
				var itemTitle = value[1];
				$(this).data('itemId', itemId);
				$(this).data('itemTitle', itemTitle);
				return value[1];
			});
			
			// add item via ajax
			$(inputId).keypress(function(e){
				var code = (e.keyCode ? e.keyCode : e.which);
				
				if(code == 13) {
					e.preventDefault();
					
					if(add_error) {
						$(errorCls).fadeOut('fast');
						$(main_container).removeClass('error');
						add_error = false;
					}
					
					if(!self.max || (self.max > tracked_items.length + tracked_new_items.length)) {
						var itemId = $(inputId).data('itemId', itemId) || null;
						var itemTitle = $(inputId).data('itemTitle', itemTitle) || null;
						
						if(!itemId){
							if(add_new_items) {
								var newItem = $(inputId).val();
								if ($.inArray(newItem, tracked_new_items) >= 0) {
									var message = "The item is already added";
									add_error = true;
									$(main_container).addClass('error', 200);
									$(errorCls).text(message).fadeIn();
									return;
								} else {
									self.add_new_item(newItem);
								}
							} else {
								var message = "Please, select item from list of choices";
								add_error = true;
								$(main_container).addClass('error', 200);
								$(errorCls).text(message).fadeIn();
								return;
							}
						} else {
							if ($.inArray(itemId, tracked_items) >= 0) {
								var message = "The item is already added";
								add_error = true;
								$(main_container).addClass('error', 200);
								$(errorCls).text(message).fadeIn();
								return;
							} else {
								self.add_item(itemId, itemTitle);
							}
						}
						$(inputId).val('');
						$(inputId).data('itemId', null);
						$(inputId).data('itemTitle', null);
					} else {
						var message = "The limit of choices are "+ self.max;
						add_error = true;
						$(main_container).addClass('error', 200);
						$(errorCls).text(message).fadeIn();
						return;
					}
				}				
			});
			
			$(formId).submit(function(){
				var items = '[';
				$.each(tracked_items, function(index, value){
					items += value +',';
				});
				items += ']';
				$(id_items).val(items);
				
				if(add_new_items) {
					var new_items = '[';
					$.each(tracked_new_items, function(index, value){
						new_items += '"'+ value +'",';
					});
					new_items += ']';
					$(id_new_items).val(new_items);
				}
			});
			
		});
	},
	
	add_item: function(id, name) {
		this.tracked_items[this.tracked_items.length] = parseInt(id);
	
		$(this.list_container).append(
			'<div id="'+ this.prefix + id +'" class="'+ this.item_container +'">' +
			'	<div class="'+ this.text +'">'+ name +'</div>' +
			'   <div class="'+ this.del +'" onclick="'+ this.id +'.remove_item('+ id +');">X</div>' +
			'</div>'
		);
	},
	
	add_new_item: function(item) {
		this.tracked_new_items[this.tracked_new_items.length] = item;

		$(this.list_container).append(
			'<div id="'+ this.prefix +'-new-'+ this.no_new_items +'" class="'+ this.item_container +'">' +
			'	<div class="'+ this.text +'">'+ item +'</div>' +
			'   <div class="'+ this.del +'" onclick="'+ this.id +'.remove_new_item('+ this.no_new_items++ +',\''+ item +'\');">X</div>' +
			'</div>'
		);
	},
	
	remove_item: function(id) {
		index = this.tracked_items.indexOf(parseInt(id));
		if (index >= 0) {
			this.tracked_items.splice(index, 1);
			$('#'+ this.prefix + id).remove();
		}
	},

	remove_new_item: function(id, item) {
		index = this.tracked_new_items.indexOf(item);
		if (index >= 0) {
			this.tracked_new_items.splice(index, 1);
			$('#'+ this.prefix +'-new-'+ id).remove();
		}
	}

});