from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter
def modulo(num, val):
    return num % val


@register.filter(name='has_group') 
def has_group(user, group_name): 
	group = Group.objects.get(name=group_name) 
	return True if group in user.groups.all() else False


@register.filter
def button_label(match, user):
	if user in match.user.all():
		return "Abmelden"
	return "Anmelden"