# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, redirect, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

from core.models import Game, Match, Team, Rules, Round
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
                msg.append(_("User account is disabled."))
        else:
            # Return an 'invalid login' error message.
            msg.append(_("Invalid username or password."))
    return render_to_response('login.html', {'errors': msg}, context_instance=context)


def movies(request):
	context = RequestContext(request)
	return render_to_response('movies.html', context_instance=context)


def pictures(request):
    context = RequestContext(request)
    return render_to_response('pictures.html', context_instance=context)


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
			elif command == "delete_team":
				delete_team(request)
			elif command == "create_tournament":
				create_tournament(request)
			elif command == "entry_round_result":
				entry_round_result(request)
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
	if create_team_type == "random":
		match.randomTeams()
	elif create_team_type == "self":
		pass
	elif create_team_type == "admin":
		pass


def delete_team(request):
	team_id = request.POST['team_id']
	Team.objects.get(id=team_id).delete()


def create_tournament(request):
	teams = Team.objects.filter(match__id=request.POST['match_id'])
	match = Match.objects.get(id=request.POST['match_id'])
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