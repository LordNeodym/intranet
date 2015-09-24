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
	var pkt_list = new Array();
	var subDataList = new Array();
	var round ;
	var counter = 2;

	/* get all Teams from Template */
	$('.tournament_tree_team').each(function() {
		if ($(this).val() != "None") {
			data.teams.push(jQuery.parseJSON($(this).val()));
		}
	});

	/* get all Points from Template */
	if ($('#tournament_bracket_mode').data('mode') == "tree") {
		$('.tournament_tree_points').each(function() {
			round = $(this).data('round');
			/* collect for 1 round */
			if (round != counter) {
				pkt_list.push(jQuery.parseJSON($(this).val()));
			}
			/* push on list and create new array for new round */
		 	else {
				data.results.push(pkt_list);
				pkt_list = new Array();
				pkt_list.push(jQuery.parseJSON($(this).val()));
				counter++;
			}
		});
	} else if ($('#tournament_bracket_mode').data('mode') == "tree_loser") {
		$('.tournament_tree_points').each(function() {
			round = $(this).data('round');
			/* new bracket */
			if (round < (counter-1)) {
				subDataList.push(pkt_list);
				data.results.push(subDataList);
				subDataList = new Array();
				pkt_list = new Array();
				pkt_list.push(jQuery.parseJSON($(this).val()));
				counter = 2;
			} 
			/* collect for 1 round */
			else if (round != counter) { 
				pkt_list.push(jQuery.parseJSON($(this).val()));
			} 
			/* push on list and create new array for new round */
			else { 
				subDataList.push(pkt_list);
				pkt_list = new Array();
				pkt_list.push(jQuery.parseJSON($(this).val()));
				counter++;
			}
		});
	}

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

	setTournamentHeight();

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


function setTournamentHeight() {
	var countTeams = $('.tournament_tree_team').length;
	
	if ($('#tournament_bracket_mode').data('mode') == "tree") {
		var calcHeight = countTeams * 34 + 45;
	} else {
		var calcHeight = (countTeams + countTeams/2) * 17 + 11;
	}
	
	$('#tournament_tree_content').css('height', calcHeight);
}

$(function() {
	var minimalData = createTeamDic();

    $('#tournament_tree_content').bracket({
		init: minimalData, 
  		save: saveFn 
  		/* data to initialize the bracket with */ 
  	})
})