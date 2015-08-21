from django.shortcuts import render_to_response
from django.template import RequestContext

from core.models import Game, Match, Team

def home(request):
	context = RequestContext(request)
	content = {}

	if request.user.is_authenticated():
		content['games'] = Game.objects.all()
	return render_to_response('home.html', {'content': content}, context_instance=context)


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