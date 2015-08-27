# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

from core.models import Game, Match, Team
from core.forms import UserForm


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


def rules(request):
	context = RequestContext(request)
	return render_to_response('rules.html', context_instance=context)


def game_site(request, slug):    
	context = RequestContext(request)
	content = {}
	if request.user.is_authenticated():
		if request.method == 'POST':
			match = Match.objects.get(id=request.POST['match_id'])
			match.save_new_user(request.user.id)
		slug = request.path.split("/")[-2]
		try:
			content['game'] = Game.objects.get(slug=slug)
		except:
			content['msg'] = "Seite nicht gefunden!"
			return render_to_response('game_site.html', {'content': content}, context_instance=context)
		content['match'] = Match.objects.filter(game=content['game'])
	else:
		content['msg'] = "Bitte zuerst einloggen!"
	return render_to_response('game_site.html', {'content': content}, context_instance=context)


@never_cache
@login_required(login_url="/login/")
def logout(request):
    auth_logout(request)
    return redirect('/')