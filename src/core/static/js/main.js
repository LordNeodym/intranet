$(document).ready(function() {
	dropdown_style();
	listenLoserBracketCheckbox();
});

function dropdown_style() {
	$( "ul.menu > li" ).each(function( index ) {
		if ($(this).children().length > 1) {
			$(this).addClass("top_menu");
		}
	});
}

function listenLoserBracketCheckbox() {
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
