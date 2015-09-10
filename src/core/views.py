# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, redirect, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

from core.models import Game, Match, Team, Rules, Round, ImageCategory, VideoCategory
from core.forms import UserForm, RoundForm


def home(request):
	context = RequestContext(request)
	content = {}
	if request.user.is_authenticated():
		content['games'] = Game.objects.exclude(match_game=None)
	else:
		content['msg'] = "Bitte zuerst einloggen!"
	return render_to_response('home.html', {'content': content}, context_instance=context)


def register(request):
    context = RequestContext(request)
    registered = False
    msg = []

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            password = request.POST['password']
            password_repeat = request.POST['password_repeat']
            if password == password_repeat:
                user = user_form.save()
                user.set_password(user.password)
                user.save()
                registered = True
            else:
                msg.append("Passwörter sind verschieden!")
        else:
            msg.append("Benutzername enthält ungültige Zeichen oder ist schon vergeben!")
    else:
        user_form = UserForm()
    return render_to_response('register.html', {'errors': msg, 'user_form': user_form, 'registered': registered}, context_instance=context)


@never_cache
def login(request):
    msg = []
    context = RequestContext(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                # Redirect to a success page.
                auth_login(request, user)
                next = request.POST['next']
                return redirect('/%s' % next)
            else:
                # Return a 'disabled account' error message
                msg.append("Benutzeraccount für {0} gesperrt.".format(user))
        else:
            # Return an 'invalid login' error message.
            msg.append("Benutzername oder Passwort falsch.")
    return render_to_response('login.html', {'errors': msg}, context_instance=context)


def menu(request):
    context = RequestContext(request)
    content = {}

    content['category'] = ImageCategory.objects.get(description="Speisekarte")
    return render_to_response('images.html', content, context_instance=context)


def videos(request):
    context = RequestContext(request)
    content = {}

    content['categories'] = VideoCategory.objects.all()
    return render_to_response('videos.html', content, context_instance=context)


def images(request):
    context = RequestContext(request)
    content = {}

    content['categories'] = ImageCategory.objects.all().exclude(description="Speisekarte")
    return render_to_response('images.html', content, context_instance=context)


def rules(request, slug):
	context = RequestContext(request)
	content = {}

	content['rule'] = Rules.objects.get(slug=slug)
	return render_to_response('rules.html', content, context_instance=context)


def game_site(request, slug, command=None):    
	context = RequestContext(request)
	content = {}
	if request.user.is_authenticated():
		if request.method == 'POST':
			if command == "register_user":
				register_user_in_match(request)
			elif command == "create_teams":
				create_teams(request)
			elif command == "create_self_team":
				content['msg'] = create_self_team(request)
			elif command == "update_self_team":
				content['msg'] = update_self_team(request)
			elif command == "create_admin_team":
				content['msg'] = create_admin_team(request)
			elif command == "delete_team":
				delete_team(request)
			elif command == "create_tournament":
				create_tournament(request)
			elif command == "entry_round_result":
				entry_round_result(request)
			elif command == "delete_tournament":
				delete_tournament(request)
			return HttpResponseRedirect(reverse('games', args=[slug]))
		try:
			content['game'] = Game.objects.get(slug=slug)
		except:
			content['msg'] = "Seite nicht gefunden!"
			return render_to_response('game_site.html', {'content': content}, context_instance=context)
		content['matches'] = Match.objects.filter(game=content['game'])

	else:
		content['msg'] = "Bitte zuerst einloggen!"
	return render_to_response('game_site.html', content, context_instance=context)


@never_cache
@login_required(login_url="/login/")
def logout(request):
    auth_logout(request)
    return redirect('/')




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
								description = number,
								match = match,
								)
		team.user.add(*teamlist)
		team.save()
	else:
		return "Spieler zur Teamerstellung nicht mehr verfügbar."


def update_self_team(request):
	teamlist = [int(x) for x in request.POST.getlist('create_self_team')]
	if set(teamlist).issubset(match.playerWithoutTeamIds()):
		team = Team.objects.get(match__id=request.POST['match_id'], user=request.user.id)
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
								description = number,
								match = match,
								)
		team.user.add(*teamlist)
		team.save()
	else:
		return "Spieler zur Teamerstellung nicht mehr verfügbar."


def delete_team(request):
	team_id = request.POST['team_id']
	Team.objects.get(id=team_id).delete()


def create_tournament(request):
	teams = Team.objects.filter(match__id=request.POST['match_id'])
	match = Match.objects.get(id=request.POST['match_id'])
	old_rounds = Round.objects.filter(match=match)
	old_rounds.delete()
	team_ids = [team.id for team in teams]
	for index, pairings in enumerate(roundRobin(team_ids)):
		for pairing in pairings:
			if not None in pairing:
				team1 = Team.objects.get(id=pairing[0])
				Round.objects.create(
								round_number = index+1,
								match = match,
								team1 = Team.objects.get(id=pairing[0]), 
								team2 = Team.objects.get(id=pairing[1])
								)


def roundRobin(units, sets=None):
    """ Generates a schedule of "fair" pairings from a list of units """
    if len(units) % 2:
        units.append(None)
    count    = len(units)
    sets     = sets or (count - 1)
    half     = count / 2
    schedule = []
    for turn in range(sets):
        pairings = []
        for i in range(half):
            pairings.append((units[i], units[count-i-1]))
        units.insert(1, units.pop())
        schedule.append(pairings)
    return schedule


def entry_round_result(request):
	form = RoundForm(data=request.POST)
	if form.is_valid():
		round = Round.objects.get(id=request.POST['round_id'])
		round.pkt1 = request.POST['pkt1']
		round.pkt2 = request.POST['pkt2']
		round.save()
		round.calcWinner()
	else:
		print form.errors


def delete_tournament(request):
	match = Match.objects.get(id=request.POST['match_id'])
	match.deleteTournament()