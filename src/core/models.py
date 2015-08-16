from django.db import models
from datetime import date, time

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
	game = models.ForeignKey(Game, verbose_name="Spiel", blank=False, null=False)
	game_mode = models.CharField(verbose_name="Modus", max_length=50, blank=True, null=True)
	player_per_team = models.IntegerField(verbose_name="Spieler pro Team", blank=False, null=False)
	description = models.CharField(verbose_name="Beschreibung", max_length=255, blank=True, null=True)

	def __unicode__(self):
		if self.game_mode:
			return u"%s - %s" % (self.game, self.game_mode)
		return u"%s" % (self.game)

	class Meta:
		verbose_name = "Match"
		verbose_name_plural = "Matches"
		ordering = ['game', 'player_per_team']


class Round(models.Model):
	match = models.ForeignKey(Match, verbose_name="Match", blank=False, null=False)
	round_number = models.IntegerField(verbose_name="Rundennummer", blank=True, null=True)
	pts_home = models.IntegerField(verbose_name="Punkte Heim", blank=False, null=False)
	pts_away = models.IntegerField(verbose_name="Punkte Gast", blank=False, null=False)
	date = models.DateField(verbose_name="Datum", blank=True, null=True)
	time = models.TimeField(verbose_name="Uhrzeit", blank=True, null=True)

	def save(self):
		if not self.id:
			self.date = date.today()
			self.time = time.now()
		super(Round, self).save()

	class Meta:
		verbose_name = "Runde"
		verbose_name_plural = "Runden"
		ordering = ['match', 'round_number']
