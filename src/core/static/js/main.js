$(document).ready(function() {
	disable_register();
	dropdown_style();
});

function dropdown_style() {
	$( "ul.menu > li" ).each(function( index ) {
		if ($(this).children().length > 1) {
			$(this).addClass("top_menu");
		}
	});
}

function disable_register() {
	$( "input" ).each(function( index ) {
		var matchId = $(this).data("matchId");
		var userId = $(this).data("userId");
		var classDef = "#user_id_"+userId+".player_name.match_id_"+matchId;

		if($(classDef).text() != "") {
			$(this).attr("disabled", true);
		}
	});
}