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
	var round ;
	var counter = 2;
	$('.tournament_tree_points').each(function() {
		round = $(this).data('round');
		if (round != counter) {
			pkt_list.push(jQuery.parseJSON($(this).val()));
			
		} else {
			data.results.push(pkt_list);
			pkt_list = new Array();
			pkt_list.push(jQuery.parseJSON($(this).val()));
			counter++;
		}
	});

	data.results.push(pkt_list);
	/*console.log(JSON.stringify(data,function(k,v){
   		if(v instanceof Array)
      		return JSON.stringify(v);
   		return v;
	},2));*/

	var data2 = {
		teams : [
		["Team 1",  "Team 2" ],
		["Team 3",  "Team 4" ],
		["Team 5",  "Team 6" ],
		["Team 7",  "Team 8" ],
		["Team 9",  "Team 10"],
		["Team 11", "Team 12"],
		["Team 13", "Team 14"],
		["Team 15", "Team 16"],
		],
		results : [[ /* WINNER BRACKET */
		[[3,5], [2,4], [6,3], [2,3], [1,5], [5,3], [7,2], [1,2]],
		[[1,2], [3,4], [5,6], [7,8]],
		[[9,1], [8,2]],
		[[1,3]]
		], [         /* LOSER BRACKET */
		[[5,1], [1,2], [3,2], [6,9]],
		[[8,2], [1,2], [6,2], [1,3]],
		[[1,2], [3,1]],
		[[3,0], [1,9]],
		[[3,2]],
		[[4,2]]
		], [         /* FINALS */
		[[3,8], [1,2]],
		[[2,1]]
		]]
	}

	var countTeams = $('.tournament_tree_team').length;
	console.log($('#tournament_bracket_mode').data('mode'));

	if ($('#tournament_bracket_mode').data('mode') == "tree") {
		var calcHeight = countTeams * 34;
	} else {
		var calcHeight = (countTeams + countTeams/2) * 17;
	}
	
	$('#tournament_tree_content').css('height', calcHeight);

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

    $('#tournament_tree_content').bracket({
		init: minimalData, 
  		save: saveFn 
  		/* data to initialize the bracket with */ 
  	})
})