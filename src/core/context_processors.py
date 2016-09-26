from core.models import IntranetMeta, Rules, Game


def intranet_processor(request):
    content = {}

    lan_name = IntranetMeta.objects.all().order_by("-lan_id")[0]
    content['lan_name'] = lan_name

    rules = Rules.objects.all()
    content['rules'] = rules

    games = Game.objects.filter(match_game__lan=lan_name).exclude(match_game=None)
    content['games'] = games

    return content

