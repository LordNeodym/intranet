# -*- coding: utf-8 -*-

from django.template import Library
from django.contrib.auth.models import Group
from django.db.models import Count

import operator

from core.models import Team

register = Library()

@register.filter
def modulo(num, val):
    return num % val

@register.filter
def devide(num, val):
    return int(num)/int(val)

@register.filter(name='has_group') 
def has_group(user, group_name): 
    group = Group.objects.get(name=group_name) 
    return True if group in user.groups.all() else False

@register.filter
def button_label(match, user):
    if user in match.user.all():
        return "Abmelden"
    return "Anmelden"

@register.filter
def button_label_self_team(match, user):
  if user in match.playerWithoutTeam():
    return "Team erstellen"
  return "Zum Team hinzufügen"

@register.filter
def get_range( value ):
  """
    Filter - returns a list containing range made from given value
    Usage (in template):

    <ul>{% for i in 3|get_range %}
      <li>{{ i }}. Do something</li>
    {% endfor %}</ul>

    Results with the HTML:
    <ul>
      <li>0. Do something</li>
      <li>1. Do something</li>
      <li>2. Do something</li>
    </ul>

    Instead of 3 one may use the variable set in the views
  """
  return range( value )

@register.filter
def splitOnSlash(folder):
    return folder.split("/")[-1]

@register.filter
def shortenString(value):
    if len(value) > 18:
        return value[:15] + "..."
    return value

@register.filter
def sortTeam(teams):
  team_dic = []
  for team in teams:
    team_dic.append([team, team.num_wins, team.num_pts])
  return sorted(team_dic, key=lambda x: (x[1], x[2]), reverse=True)

@register.filter
def radioCheckedTeam(match, button_label):
  if match.team_choose_type == button_label:
    return "checked"

@register.filter
def radioCheckedTour(match, button_label):
  if match.tour_choose_type == button_label:
    return "checked"

@register.filter
def getListElement(list, element):
  return list[element]

@register.filter
def getName(user):
  if user.first_name and user.last_name:
    return "{0} {1}.".format(user.first_name, user.last_name[0])
  elif user.first_name:
    return user.first_name
  else:
    return user

@register.filter
def getIP(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    elif request.META.get('HTTP_X_REAL_IP'):
        ip = request.META.get('HTTP_X_REAL_IP')
    else:
        ip = request.META.get('REMOTE_ADDR')
    print request.META.get('HTTP_X_FORWARDED_FOR'), request.META.get('HTTP_X_REAL_IP'), request.META.get('REMOTE_ADDR')
    return ip

@register.filter
def sort_by(queryset, order):
    return queryset.order_by(order)
