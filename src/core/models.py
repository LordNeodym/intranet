# -*- coding: utf-8 -*-

from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from django.core.validators import  MinValueValidator, MaxValueValidator
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

from filer.fields.file import FilerFileField
from filer.fields.image import FilerImageField

from random import shuffle
from datetime import datetime

from core.validators import integer_only


class IntranetMeta(models.Model):
    name = models.CharField(verbose_name="LAN Name", max_length=50, default="Intranet", null=False, blank=False)
    lan_id = models.PositiveIntegerField(verbose_name="LAN ID", unique=True)
    title = models.CharField(verbose_name="Begrüßungstext", max_length=128, default="Herzlich Willkommen im Intranet", null=True, blank=True)
    description = models.TextField(verbose_name="Beschreibung", max_length=1024, null=True, blank=True)
    date = models.DateField(verbose_name="Beginn der LAN")
    image_upload_allowed = models.BooleanField(verbose_name="Alle User dürfen Bilder hochladen?", default=True)
    video_upload_allowed = models.BooleanField(verbose_name="Alle User dürfen Videos hochladen?", default=True)
    active = models.BooleanField(verbose_name="Aktiv?", default=False)

    def __unicode__(self):
        return u"%s" % (self.name)

    class Meta:
        verbose_name = "Intranet Metadaten"
        verbose_name_plural = "Intranet Metadaten"
        app_label = "core"
        ordering = ["-lan_id"]


class UserExtension(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthdate = models.DateField(verbose_name="Geburtstag", null=True, blank=True)
    avatar = models.ImageField(verbose_name="Avatar", upload_to="user_avatar", blank=True, null=True)
    seat = models.CharField(verbose_name="Sitzplatz", max_length=63, null=True, blank=True)
    ip = models.GenericIPAddressField(verbose_name="IP-Adresse", null=True, blank=True)
    participated_lans = models.ManyToManyField(IntranetMeta, verbose_name="Teilgenommene LANs", blank=True, related_name="user_lan")

    @property
    def shortenName(self):
        if len(self.user.username) > 12:
            return "{0}...".format(self.user.username[:13])
        return self.user.username

    def has_user(self):
        return self.user_id is not None

    def delete(self, *args, **kwargs):
        # You have to prepare what you need before delete the model
        storage, path = self.avatar.storage, self.avatar.path
        # Delete the model before the file
        super(UserExtension, self).delete(*args, **kwargs)
        # Delete the file after the model
        storage.delete(path)

    class Meta:
        verbose_name = "Zusätzliche Angaben"
        verbose_name_plural = "Zusätzliche Angaben"
        app_label = "core"


class Software(models.Model):
    name = models.CharField(verbose_name="Name", max_length=255, null=False, blank=False)
    file = models.FileField(verbose_name="Dateiupload", upload_to='software')
    description = models.TextField(verbose_name="Beschreibung", max_length=255, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u"%s" % (self.name)

    class Meta:
        verbose_name = "Software"
        verbose_name_plural = "Software"
        app_label = "core"


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
        app_label = "core"


class RulesInline(models.Model):
    rules = models.ForeignKey(Rules, verbose_name="Regelgruppe", blank=True, null=True, related_name="inline_rules")
    information = models.TextField(verbose_name="Regel", max_length=512, null=True, blank=True)

    def __unicode__(self):
        return u"%s" % (self.information)

    class Meta:
        verbose_name = "Regel"
        verbose_name_plural = "Regeln"
        app_label = "core"


class Game(models.Model):
    name = models.CharField(verbose_name="Name", max_length=30, unique=True, blank=False, null=False)
    description = models.TextField(verbose_name="Beschreibung / Installationsanleitung", max_length=1024, blank=True, null=True)
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
        app_label = "core"


class Match(models.Model):
    TEAM_CHOOSE_TYPE = (
        ('None', 'Bitte wählen'),
        ('rand', 'Zufalls Wahl'),
        ('self', 'Eigene Wahl'),
        ('admin', 'Admin Wahl'),
    )
    TOUR_CHOOSE_TYPE = (
        ('None', 'Bitte wählen'),
        ('vs', 'Jeder gegen Jeden'),
        ('tree', 'Turnierbaum'),
        ('tree_loser', 'Turnierbaum mit Loserbracket'),
    )

    lan = models.ForeignKey(IntranetMeta, verbose_name="LAN", related_name="match_lan")
    game = models.ForeignKey(Game, verbose_name="Spiel", blank=False, null=False, related_name="match_game")
    game_mode = models.CharField(verbose_name="Modus", max_length=50, blank=True, null=True)
    player_per_team = models.IntegerField(verbose_name="Spieler pro Team", blank=False, null=False, validators=[MinValueValidator(1)])
    description = models.TextField(verbose_name="Beschreibung", max_length=255, blank=True, null=True)
    user = models.ManyToManyField(User, verbose_name="Spieler", blank=True, related_name="match_user")
    datetime = models.DateTimeField(verbose_name="Startzeit", blank=True, null=True, default=datetime.now)
    team_choose_type = models.CharField(verbose_name="Team Wahl", editable=False, max_length=5, choices=TEAM_CHOOSE_TYPE, default="None", blank=True)
    tour_choose_type = models.CharField(verbose_name="Turnier Wahl", editable=False, max_length=10, choices=TOUR_CHOOSE_TYPE, default="None", blank=True)
    rules = models.TextField(verbose_name="Spielregeln", max_length=1024, null=True, blank=True)

    def __unicode__(self):
        if self.game_mode:
            return u"%s (%svs%s) - %s" % (self.game, self.player_per_team, self.player_per_team, self.game_mode)
        return u"%s (%svs%s)" % (self.game, self.player_per_team, self.player_per_team)

    @property
    def tournamentBracketRounds(self):
        tour_bracket_list = []
        counter = len(self.team_match.all())
        n = counter/2
        round_number = 1

        while counter != 0: 
            if counter <= n:
                n = n/2
                round_number += 1
            tour_bracket_list.append(round_number)
            counter -= 1
        tour_bracket_list[-1] -= 1

        return tour_bracket_list
    
    @property
    def tournamentBracketRoundsWLoser(self):
        tour_bracket_list = []

        # WINNER Bracket
        tour_bracket_list = self.tournamentBracketRounds
        tour_bracket_list.pop()

        # LOSER Bracket
        counter = len(self.team_match.all())
        n = counter*3/4
        round_number = 1
        double_count = True

        while counter > 2: 
            if counter <= n:
                round_number += 1
                if not double_count:
                    n = n*3/4
                    double_count = True
                else:
                    n = n*2/3
                    double_count = False
            tour_bracket_list.append(round_number)
            counter -= 1

        # FINALS
        tour_bracket_list.extend([1,1,2])

        return tour_bracket_list

    def matchDesciption(self):
        if self.game_mode:
            return u"%svs%s (%s)" % (self.player_per_team, self.player_per_team, self.game_mode)
        return u"%svs%s" % (self.player_per_team, self.player_per_team)

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
        if self.player_per_team == 1:
            for user in users:
                team = Team.objects.create(match=self, description=user.username)
                team.save()
                team.user.add(user)
        else:
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

        """ delete settings """
        self.team_choose_type = "None"
        self.tour_choose_type = "None"
        self.save()


    class Meta:
        verbose_name = "Match"
        verbose_name_plural = "Matches"
        ordering = ['game', 'datetime']
        app_label = "core"


#class MatchRulesInline(models.Model):
#   match = models.ForeignKey(Match, verbose_name="Spielregeln", blank=True, null=True, related_name="inline_rules")
#   information = models.TextField(verbose_name="Regel", max_length=512, null=True, blank=True)
#
#   def __unicode__(self):
#       return u"%s" % (self.information)
#
#   class Meta:
#       verbose_name = "Spielregel"
#       verbose_name_plural = "Spielregeln"


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
        try: 
            description = int(self.description)
            return "Team {0}".format(description)
        except:
            return "{0}".format(self.description)

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
        ordering = ['id']
        app_label = "core"


class Round(models.Model):
    match = models.ForeignKey(Match, verbose_name="Match", blank=False, null=False, related_name="round_match")
    round_number = models.IntegerField(verbose_name="Rundennummer", blank=True, null=True)
    team1 = models.ForeignKey(Team, verbose_name="Team Heim", blank=True, null=True, related_name="round_team1")
    team2 = models.ForeignKey(Team, verbose_name="Team Gast", blank=True, null=True, related_name="round_team2")
    pkt1 = models.IntegerField(verbose_name="Punkte Heim", blank=True, null=True, validators=[integer_only])
    pkt2 = models.IntegerField(verbose_name="Punkte Gast", blank=True, null=True, validators=[integer_only])
    datetime = models.DateTimeField(verbose_name="Datum/Uhrzeit", blank=True, null=True)
    winner = models.ForeignKey(Team, editable=False, null=True, related_name="round_win")

    def save(self, *args, **kwargs):
        self.calcWinner()
        super(Round, self).save(*args, **kwargs)

    def __unicode__(self):
        if self.round_number:
            return u"Runde %s - %s vs. %s" % (self.round_number, self.team1, self.team2)
        return u"%s vs. %s" % (self.team1, self.team2)

    def getNumberOfSameRounds(self):
        return len(Round.objects.filter(match = self.match, round_number = self.round_number))

    def calcWinner(self):
        if self.pkt1 and self.pkt2:
            if int(self.pkt1) > int(self.pkt2):
                self.winner = self.team1
            elif int(self.pkt2) > int(self.pkt1):
                self.winner = self.team2
            else:
                self.winner = None
            #self.save()

    @property
    def getTeams(self):
        if self.team1 and self.team2:
            return '["{0}", "{1}"]'.format(self.team1.getTeam, self.team2.getTeam)
        return

    @property
    def getPoints(self):
        return '["{0}", "{1}"]'.format(self.pkt1, self.pkt2)

    """ prevent showing the input 'None' in the Field for points """
    @property
    def getPkt1(self):
        if self.pkt1 == None:
            return ""
        return self.pkt1

    """ prevent showing the input 'None' in the Field for points """
    @property
    def getPkt2(self):
        if self.pkt2 == None:
            return ""
        return self.pkt2

    @property
    def getDatetime(self):
        if self.datetime:
            return self.datetime
        return "-"

    class Meta:
        verbose_name = "Runde"
        verbose_name_plural = "Runden"
        ordering = ['round_number', 'datetime']
        app_label = "core"


class VideoCategory(models.Model):
    description = models.CharField(verbose_name="Kategorie", max_length=50, blank=False, null=False, unique=True)

    def __unicode__(self):
        return u"%s" % (self.description)

    class Meta:
        verbose_name = "Videokategorie"
        verbose_name_plural = "Videokategorien"
        app_label = "core"


class SingleVideo(models.Model):
    category = models.ForeignKey(VideoCategory, null=False, related_name="video_videocategory")
    video = FilerFileField(verbose_name="Video", related_name="video", blank=False, null=False)

    def __unicode__(self):
        return u"%s" % (self.video)

    class Meta:
        verbose_name = "Video"
        verbose_name_plural = "Videos"
        app_label = "core"


class ImageCategory(models.Model):
    description = models.CharField(verbose_name="Kategorie", max_length=50, blank=False, null=False, unique=True)

    def __unicode__(self):
        return u"%s" % (self.description)

    class Meta:
        verbose_name = "Bilderkategorie"
        verbose_name_plural = "Bilderkategorien"
        app_label = "core"


class SingleImage(models.Model):
    category = models.ForeignKey(ImageCategory, null=False, related_name="image_imagecategory")
    image = FilerImageField(verbose_name="Image", related_name="image", blank=False, null=False)

    def __unicode__(self):
        return u"%s" % (self.image)

    class Meta:
        verbose_name = "Bild"
        verbose_name_plural = "Bilder"
        app_label = "core"


class MenuOrder(models.Model):
    description = models.CharField(verbose_name="Name",max_length=255, null=False, blank=False, default="Pizzeria")
    timestamp = models.DateTimeField(verbose_name="Datum", null=False, blank=False)
    venue = models.CharField(verbose_name="Ort", max_length=255, null=True, blank=True)
    locked = models.BooleanField(verbose_name="Bestellung sperren?", default=False)

    def __unicode__(self):
        formatedTime = self.timestamp.strftime("%A %d.%m.%Y - %H:%M")
        if self.venue:
            return u"%s - %s - %s" % (self.description, formatedTime, self.venue)
        return u"%s - %s" % (self.description, formatedTime)

    class Meta:
        verbose_name = "Bestellung"
        verbose_name_plural = "Bestellungen"
        ordering = ['-timestamp']
        app_label = "core"


class SingleMenuOrder(models.Model):
    order = models.ForeignKey(MenuOrder, verbose_name="Bestellung", null=False, blank=False)
    name = models.ForeignKey(User, verbose_name="Benutzer", null=False, blank=False)
    order_number = models.CharField(verbose_name="Bestellnummer", max_length=255, null=False, blank=False)
    extra = models.CharField(verbose_name="Extra", max_length=255, null=True, blank=True)
    price = models.FloatField(verbose_name="Preis", null=True, blank=True, validators = [MinValueValidator(0), MaxValueValidator(99.99)])

    def __unicode__(self):
        return u"%s - %s" % (self.order, self.name)

    @classmethod
    def create(self, order, userId, order_number, extra, price):
        if order_number:
            try:
                user = User.objects.get(id=userId)
                SingleMenuOrder.objects.create(order=order, name=user, order_number=order_number, extra=extra, price=price)
                return None
            except Exception as e:
                error = {'msg': 'Bitte Eingaben überprüfen', 'exception': e}
                return error
        else:
            error = {'msg': 'Bitte eine Bestellnummer eingeben'}
            return error

    class Meta:
        verbose_name = "Einzel-Bestellung"
        verbose_name_plural = "Einzel-Bestellungen"
        ordering = ['-order', '-name']
        app_label = "core"