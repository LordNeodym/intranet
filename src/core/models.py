# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify
from django.core import validators
from django.db.models import Q
from django.db.models import Sum

from filer.fields.file import FilerFileField
from filer.fields.image import FilerImageField

from random import shuffle
from datetime import date, datetime

from core.validators import integer_only


def validate_only_one_instance(obj):
	model = obj.__class__
	if (model.objects.count() > 0 and obj.id != model.objects.get().id):
		raise ValidationError("Nur eine Instanz von %s erlaubt!" % model.__name__)


class IntranetMeta(models.Model):
	name = models.CharField(verbose_name="LAN Name", max_length=50, default="Intranet", null=False, blank=False)
	title = models.CharField(verbose_name="Begrüßungstext", max_length=128, default="Herzlich Willkommen im Intranet", null=True, blank=True)
	description = models.TextField(verbose_name="Beschreibung", max_length=1024, null=True, blank=True)

	def clean(self):
		validate_only_one_instance(self)

	def __unicode__(self):
		return u"%s" % (self.name)

	class Meta:
		verbose_name = "Intranet Metadaten"
		verbose_name_plural = "Intranet Metadaten"


class Rules(models.Model):
	name = models.CharField(verbose_name="Regelgruppe", max_length=30, null=False, unique=True, blank=False, default="Allgemeine Regeln")
	slug = models.SlugField(verbose_name="Slug", blank=True, unique=True, editable=False)

	def __unicode__(self):
		return u"%s" % (self.name)

	def save(self):
		self.slug = slugify(self.name)
		super(Rules,self).save()

	class Meta:
		verbose_name = "Regelgruppe"
		verbose_name_plural = "Regelgruppen"


class RulesInline(models.Model):
	rules = models.ForeignKey(Rules, verbose_name="Regelgruppe", blank=True, null=True, related_name="inline_rules")
	information = models.TextField(verbose_name="Regel", max_length=512, null=True, blank=True)

	def __unicode__(self):
		return u"%s" % (self.information)

	class Meta:
		verbose_name = "Regel"
		verbose_name_plural = "Regeln"


class Game(models.Model):
	name = models.CharField(verbose_name="Name", max_length=50, unique=True, blank=False, null=False)
	slug = models.SlugField(verbose_name="Slug", blank=True, unique=True, editable=False)
	icon = FilerImageField(verbose_name="Icon", related_name="game_icon", blank=True, null=True)

	def __unicode__(self):
		return u"%s" % (self.name)

	def save(self):
		self.slug = slugify(self.name)
		super(Game,self).save()

	class Meta:
		verbose_name = "Spiel"
		verbose_name_plural = "Spiele"
		ordering = ['name']


class Match(models.Model):
	TEAM_CHOOSE_TYPE = (
		('None', 'Bitte wählen'),
	    ('rand', 'Zufalls Wahl'),
	    ('self', 'Eigene Wahl'),
	    ('admin', 'Admin Wahl'),
	)

	game = models.ForeignKey(Game, verbose_name="Spiel", blank=False, null=False, related_name="match_game")
	game_mode = models.CharField(verbose_name="Modus", max_length=50, blank=True, null=True)
	player_per_team = models.IntegerField(verbose_name="Spieler pro Team", blank=False, null=False)
	description = models.TextField(verbose_name="Beschreibung", max_length=255, blank=True, null=True)
	user = models.ManyToManyField(User, verbose_name="Spieler", related_name="match_user")
	datetime = models.DateTimeField(verbose_name="Datum/Uhrzeit", blank=True, null=True)
	team_choose_type = models.CharField(verbose_name="Team Wahl", max_length=5, choices=TEAM_CHOOSE_TYPE, default="None")

	def __unicode__(self):
		if self.game_mode:
			return u"%s (%svs.%s) - %s" % (self.game, self.player_per_team, self.player_per_team, self.game_mode)
		return u"%s (%svs.%s)" % (self.game, self.player_per_team, self.player_per_team)

	def getNewTeamNumber(self):
		teams = self.team_match.all().order_by('-description')
		try:
			return int(teams[0].description) + 1
		except IndexError:
			return 1

	def playerWithoutTeam(self):
		player_list = []
		exclude_list = []
		teams = self.team_match.all()
		for team in teams:
			exclude_list.append(team.user.all())
		exclude_list = [item for sublist in exclude_list for item in sublist]
		for user in self.user.all():
			if not user in exclude_list:
				player_list.append(user)
		return player_list

	def playerWithoutTeamIds(self):
		player_list = []
		for user in self.playerWithoutTeam():
			player_list.append(user.id)
		return player_list

	def save_new_user(self, user_id):
		self.user.add(User.objects.get(id=user_id))
		self.save()

	def rem_new_user(self, user_id):
		self.user.remove(User.objects.get(id=user_id))
		self.save()	

	def button_label(self, user_id):
		user = User.objects.get(id=user_id)
		if user in self.user.all():
			return "Abmelden"
		return "Anmelden"
		
	def randomTeams(self):
		""" delete all teams """
		teams = self.team_match.all()
		teams.delete()

		""" create random teams """
		users = list(self.user.all())
		shuffle(users)
		counter = 0
		for index, user in enumerate(users):
			if index % self.player_per_team == 0:
				counter += 1
				team = Team.objects.create(match=self, description=counter)
				team.save()
			team.user.add(user)

	def deleteTournament(self):
		""" delete all rounds """
		rounds = self.round_match.all()
		rounds.delete()

		""" delete all teams """
		teams = self.team_match.all()
		teams.delete()


	class Meta:
		verbose_name = "Match"
		verbose_name_plural = "Matches"
		ordering = ['game', 'datetime']


class MatchRulesInline(models.Model):
	match = models.ForeignKey(Match, verbose_name="Spielregeln", blank=True, null=True, related_name="inline_rules")
	information = models.TextField(verbose_name="Regel", max_length=512, null=True, blank=True)

	def __unicode__(self):
		return u"%s" % (self.information)

	class Meta:
		verbose_name = "Spielregel"
		verbose_name_plural = "Spielregeln"


class Team(models.Model):
	description = models.CharField(verbose_name="Teamname", max_length=50, blank=True, null=True)
	match = models.ForeignKey(Match, verbose_name="Match", related_name="team_match")
	user = models.ManyToManyField(User, verbose_name="Spieler", related_name="team_user")

	def __unicode__(self):
		user_list = []
		for u in self.user.all():
			user_list.append(str(u.username))
		if self.description:
			return u"%s - (Team %s) - %s" % (self.match, self.description, user_list)
		return u"%s - %s" % (self.match, user_list)

	@property	
	def getTeam(self):
		return u"Team {0}".format(self.description)

	@property
	def num_wins(self):
		num_wins = Round.objects.filter(winner=self).count()
		return num_wins

	@property
	def num_pts(self):
		num_pts_t1 = Round.objects.filter(team1=self)\
				.aggregate(Sum('pkt1'))
		num_pts_t2 = Round.objects.filter(team2=self)\
				.aggregate(Sum('pkt2'))
		sum = 0
		try:
			sum += int(num_pts_t1['pkt1__sum'])
		except TypeError:
			pass
		try:
			sum += int(num_pts_t2['pkt2__sum'])
		except TypeError:
			pass
		return sum

	class Meta:
		verbose_name = "Team"
		verbose_name_plural = "Teams"
		ordering = ['description']

class Round(models.Model):
	match = models.ForeignKey(Match, verbose_name="Match", blank=False, null=False, related_name="round_match")
	round_number = models.IntegerField(verbose_name="Rundennummer", blank=True, null=True)
	team1 = models.ForeignKey(Team, verbose_name="Team Heim", blank=False, null=False, related_name="round_team1")
	team2 = models.ForeignKey(Team, verbose_name="Team Gast", blank=False, null=False, related_name="round_team2")
	pkt1 = models.IntegerField(verbose_name="Punkte Heim", blank=True, null=True, validators=[integer_only])
	pkt2 = models.IntegerField(verbose_name="Punkte Gast", blank=True, null=True, validators=[integer_only])
	datetime = models.DateTimeField(verbose_name="Datum/Uhrzeit", blank=True, null=True)
	winner = models.ForeignKey(Team, editable=False, null=True, related_name="round_win")

	def __unicode__(self):
		if self.round_number:
			return u"Runde %s - %s vs. %s" % (self.round_number, self.team1, self.team2)
		return u"%s vs. %s" % (self.team1, self.team2)

	def getNumberOfSameRounds(self):
		return len(Round.objects.filter(match = self.match, round_number = self.round_number))

	def calcWinner(self):
		if int(self.pkt1) > int(self.pkt2):
			self.winner = self.team1
		elif int(self.pkt2) > int(self.pkt1):
			self.winner = self.team2
		else:
			self.winner = None
		self.save()

	@property
	def getPkt1(self):
		if self.pkt1:
		    return self.pkt1
		return ""

	@property
	def getPkt2(self):
		if self.pkt2:
		    return self.pkt2
		return ""

	@property
	def getDatetime(self):
	    if self.datetime:
	    	return self.datetime
	    return "-"

	class Meta:
		verbose_name = "Runde"
		verbose_name_plural = "Runden"
		ordering = ['round_number', 'datetime']