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


function saveFn(data, userData) {
	var json = JSON.stringify(data)
	var match_id;
	$('.tournament_tree_team').each(function() {
		match_id = $(this).data('match');
		return false;
	});
	saveTournamentBracket(json, match_id);
}


function createTeamDic() {
	var data = {teams : [], results : []}
	/* get all Teams from Template */
	$('.tournament_tree_team').each(function() {
		if ($(this).val() != "None") {
			data.teams.push(jQuery.parseJSON($(this).val()));
		}
	});

	var pkt_list = new Array();
	var round;
	var counter = 1;
	$('.tournament_tree_points').each(function() {
		if (round == counter) {
			counter++;
		}
		round = $(this).data('round');
		pkt_list.push(jQuery.parseJSON($(this).val()));
		if (round != counter) {
			data.results.push(pkt_list);
			pkt_list = new Array();
		}
	});

	console.log(JSON.stringify(data,function(k,v){
   if(v instanceof Array)
      return JSON.stringify(v);
   return v;
},2));

	return data;

	/*{
	    teams : [
	      ["Team 1", "Team 2"], first matchup 
	      ["Team 3", "Team 4"]  second matchup
	    ],
	    results : [
	      [[,], [,]],       first round
	      [[,], [,]]        second round
	    ]
  	}*/
}


$(function() {
	var minimalData = createTeamDic();

    $('#tournamen_tree_content').bracket({
		init: minimalData, 
  		save: saveFn 
  		/* data to initialize the bracket with */ 
  	})
})