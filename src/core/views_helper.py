# -*- coding: utf-8 -*-

from django.conf import settings

from random import shuffle

from core.models import IntranetMeta, Match, Team, Round
from core.forms import RoundForm

"""
Helper Functions
"""

def register_user_in_match(request):
    match = Match.objects.get(id=request.POST['match_id'])
    if request.user in match.user.all():
        match.rem_new_user(request.user.id)
    else:
        match.save_new_user(request.user.id)


def create_teams(request):
    if not "create_team_type" in request.POST:
        return "Erstellungstyp für Teams nicht ausgewählt."
    create_team_type = request.POST['create_team_type']
    match = Match.objects.get(id=request.POST['match_id'])
    match.deleteTournament()
    if create_team_type == "random":
        match.team_choose_type = "rand"
        match.save()
        match.randomTeams()
    elif create_team_type == "self":
        match.team_choose_type = "self"
        match.save()
    elif create_team_type == "admin":
        match.team_choose_type = "admin"
        match.save()


def create_self_team(request):
    teamlist = [int(x) for x in request.POST.getlist('create_self_team')]
    if not teamlist:
        return
    teamlist.append(request.user.id)
    match = Match.objects.get(id=request.POST['match_id'])

    if set(teamlist).issubset(match.playerWithoutTeamIds()):
        number = match.getNewTeamNumber()
        team = Team.objects.create(
            description=number,
            match=match,
        )
        team.user.add(*teamlist)
        team.save()
    else:
        return "Spieler zur Teamerstellung nicht mehr verfügbar."


def update_self_team(request):
    teamlist = [int(x) for x in request.POST.getlist('create_self_team')]
    match = Match.objects.get(id=request.POST['match_id'])
    if set(teamlist).issubset(match.playerWithoutTeamIds()):
        team = Team.objects.get(
            match__id=request.POST['match_id'], user=request.user.id)
        team.user.add(*teamlist)
        team.save()
    else:
        return "Spieler zur Teamerstellung nicht mehr verfügbar."


def create_admin_team(request):
    teamlist = [int(x) for x in request.POST.getlist('create_admin_team')]
    if not teamlist:
        return
    match = Match.objects.get(id=request.POST['match_id'])
    if set(teamlist).issubset(match.playerWithoutTeamIds()):
        number = match.getNewTeamNumber()
        team = Team.objects.create(
            description=number,
            match=match,
        )
        team.user.add(*teamlist)
        team.save()
    else:
        return "Spieler zur Teamerstellung nicht mehr verfügbar."


def delete_team(request):
    team_id = request.POST['team_id']
    Team.objects.get(id=team_id).delete()


def create_tournament(request):
    if not "create_tour" in request.POST:
        return "Erstellungstyp für das Turnier nicht ausgewählt."

    teams = Team.objects.filter(match__id=request.POST['match_id'])
    match = Match.objects.get(id=request.POST['match_id'])
    old_rounds = Round.objects.filter(match=match)
    old_rounds.delete()
    team_ids = [team.id for team in teams]

    if request.POST['create_tour'] == "vs":
        create_tournament_vs(match, team_ids)
    elif request.POST['create_tour'] == "tree":
        create_tournament_tree(request, match, team_ids)


def create_tournament_vs(match, team_ids):
    match.tour_choose_type = "vs"
    match.save()
    for index, pairings in enumerate(roundRobin(team_ids)):
        for pairing in pairings:
            if not None in pairing:
                Round.objects.create(
                    round_number=index+1,
                    match=match,
                    team1=Team.objects.get(id=pairing[0]),
                    team2=Team.objects.get(id=pairing[1])
                )


def roundRobin(units, sets=None):
    """ Generates a schedule of "fair" pairings from a list of units """
    if len(units) % 2:
        units.append(None)
    count = len(units)
    sets = sets or (count - 1)
    half = count / 2
    schedule = []
    for turn in range(sets):
        pairings = []
        for i in range(half):
            pairings.append((units[i], units[count-i-1]))
        units.insert(1, units.pop())
        schedule.append(pairings)
    return schedule


def create_tournament_tree(request, match, team_ids):
    if not len(team_ids) in settings.ALLOWED_TOURNAMENT_TREE_TEAMS:
        return "Aus der Anzahl der Teams lässt sich kein Turnierbaum bauen."

    shuffle(team_ids)
    current_index = 0

    """ first round """
    for index, team in enumerate(team_ids):
        current_index = index+1
        Round.objects.create(
            round_number=current_index,
            match=match,
            team1=Team.objects.get(id=team),
            team2=Team.objects.get(id=team_ids.pop())
        )

    """ list team_ids is now half the size of the origin, cause of pop() """
    """ dummy rounds after first round"""
    if "create_tour_tree_loserbracket" in request.POST:
        match.tour_choose_type = "tree_loser"
        match.save()
        """ WINNER BRACKET """
        for ele in range(len(team_ids) - 1):
            current_index += 1
            Round.objects.create(
                round_number=current_index,
                match=match
            )

        """ LOSER BRACKET """
        while not len(team_ids) == 1:
            for ele in range(len(team_ids)):
                current_index += 1
                Round.objects.create(
                    round_number=current_index,
                    match=match
                )
            team_ids = team_ids[::2]

        """ FINALS """
        for ele in range(3):
            current_index += 1
            Round.objects.create(
                round_number=current_index,
                match=match
            )
    else:
        match.tour_choose_type = "tree"
        match.save()
        """ WINNER BRACKET + FINALS """
        for ele in range(len(team_ids)):
            current_index += 1
            Round.objects.create(
                round_number=current_index,
                match=match
            )


def entry_round_result(request):
    form = RoundForm(data=request.POST)
    if form.is_valid():
        round = Round.objects.get(id=request.POST['round_id'])
        if request.POST['pkt1'] == "":
            round.pkt1 = None
        else:
            round.pkt1 = request.POST['pkt1']
        if request.POST['pkt2'] == "":
            round.pkt2 = None
        else:
            round.pkt2 = request.POST['pkt2']
        round.save()
    else:
        print form.errors


def delete_tournament(request):
    match = Match.objects.get(id=request.POST['match_id'])
    match.deleteTournament()


def getCurrentLAN():
    activeMeta = IntranetMeta.objects.filter(active=True)
    if activeMeta:
        return activeMeta[0]
    return IntranetMeta.objects.all().order_by("-lan_id")[0]


def getIP(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    elif request.META.get('HTTP_X_REAL_IP'):
        ip = request.META.get('HTTP_X_REAL_IP')
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
