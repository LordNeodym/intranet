from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

from core.models import Game, Match, Team


def home(request):
	context = RequestContext(request)
	content = {}
	if request.user.is_authenticated():
		content['games'] = Game.objects.exclude(match_game=None)
	else:
		content['msg'] = "Bitte zuerst einloggen!"
	return render_to_response('home.html', {'content': content}, context_instance=context)


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
    return render_to_response('login.html', {'errors': msg}, context)


def game_site(request, slug):    
	context = RequestContext(request)
	content = {}
	if request.user.is_authenticated():
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
    return redirect('/home/')