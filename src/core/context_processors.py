from core.models import IntranetMeta


def intranet_processor(request):
	lan_name = IntranetMeta.objects.all()[0]          
	return {'lan_name': lan_name}