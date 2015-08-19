from django.db import models
from datetime import date, datetime
from django.contrib.auth.models import User


class Game(models.Model):
	name = models.CharField(verbose_name="Name", max_length=50, unique=True, blank=False, null=False)
	slug = models.SlugField(verbose_name="Slug", unique=True)
	img = models.ImageField(verbose_name="Icon", upload_to="game_icon", blank=True, null=True)

	def __unicode__(self):
		return u"%s" % (self.name)

	class Meta:
		verbose_name = "Spiel"
		verbose_name_plural = "Spiele"
		ordering = ['name']


class Match(models.Model):
	game = models.ForeignKey(Game, verbose_name="Spiel", blank=False, null=False, related_name="match_game")
	game_mode = models.CharField(verbose_name="Modus", max_length=50, blank=True, null=True)
	player_per_team = models.IntegerField(verbose_name="Spieler pro Team", blank=False, null=False)
	description = models.CharField(verbose_name="Beschreibung", max_length=255, blank=True, null=True)
	user = models.ManyToManyField(User, verbose_name="Spieler", related_name="match_user")

	def __unicode__(self):
		if self.game_mode:
			return u"%s (%svs.%s) - %s" % (self.game, self.game_mode, self.player_per_team, self.player_per_team)
		return u"%s (%svs.%s)" % (self.game, self.player_per_team, self.player_per_team)

	class Meta:
		verbose_name = "Match"
		verbose_name_plural = "Matches"
		ordering = ['game', 'player_per_team']


class Team(models.Model):
	description = models.CharField(verbose_name="Teamname", max_length=50, blank=True, null=True)
	match = models.ForeignKey(Match, verbose_name="Match", related_name="team_match")
	user = models.ManyToManyField(User, verbose_name="Spieler", related_name="team_user")

	def __unicode__(self):
		#print self.user()
		user_list = []
		for u in self.user.all():
			user_list.append(str(u.username))
		if self.description:
			return u"%s (%s)" % (self.user, self.description)
		return u"%s - %s" % (self.match, user_list)

	def getTeam(self):
		return self.__unicode__()

	class Meta:
		verbose_name = "Team"
		verbose_name_plural = "Teams"


class Round(models.Model):
	round_number = models.IntegerField(verbose_name="Rundennummer", blank=True, null=True)
	team1 = models.ForeignKey(Team, verbose_name="Team Heim", blank=False, null=False, related_name="round_team1")
	team2 = models.ForeignKey(Team, verbose_name="Team Gast", blank=False, null=False, related_name="round_team2")
	pkt1 = models.IntegerField(verbose_name="Punkte Heim", blank=False, null=False)
	pkt2 = models.IntegerField(verbose_name="Punkte Gast", blank=False, null=False)
	date = models.DateField(verbose_name="Datum", blank=True, null=True)
	time = models.TimeField(verbose_name="Uhrzeit", blank=True, null=True)

	def save(self):
		if not self.id:
			self.date = date.today()
			self.time = datetime.now().time()
		super(Round, self).save()

	def __unicode__(self):
		if self.round_number:
			return u"Runde %s - %s vs. %s" % (self.round_number, team1, team2)
		return u"%s vs. %s" % (team1, team2)

	class Meta:
		verbose_name = "Runde"
		verbose_name_plural = "Runden"
		ordering = ['round_number']