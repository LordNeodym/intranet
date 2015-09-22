$(document).ready(function() {
	dropdown_style();
	listenLoserBracketCheckbox();
	fancybox();
});


function dropdown_style() {
	$( "ul.menu > li" ).each(function( index ) {
		if ($(this).children().length > 1) {
			$(this).addClass("top_menu");
		}
	});
}


function listenLoserBracketCheckbox() {
	if ($("#create_tour_tree").is(':checked')) {
		$("#create_tour_tree_loserbracket").prop('disabled', false);
	}

	$("#create_tour_vs").click(function() {
		if ($("#create_tour_vs").is(':checked')) {
			$("#create_tour_tree_loserbracket").prop('checked', false);
			$("#create_tour_tree_loserbracket").prop('disabled', true);
		}
	});

	$("#create_tour_tree").click(function() {
		if ($("#create_tour_tree").is(':checked')) {
			$("#create_tour_tree_loserbracket").prop('disabled', false);
		}
	});
}


function fancybox() {
	/* This is basic - uses default settings */
	
	$("a#single_image").fancybox();
	
	/* Using custom settings */
	
	$("a#inline").fancybox({
		'hideOnContentClick': true
	});

	/* Apply fancybox to multiple items */
	
	$("a.group").fancybox({
		'transitionIn'	:	'elastic',
		'transitionOut'	:	'elastic',
		'speedIn'		:	600, 
		'speedOut'		:	200, 
		'overlayShow'	:	false
	});
}
