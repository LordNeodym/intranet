$(document).ready(function() {
	disable_register();
});

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