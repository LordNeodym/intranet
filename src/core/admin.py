from django.contrib import admin
from core.models import Game, Match, Round, Team, TeamRound

class TeamAdmin(admin.ModelAdmin):
	list_display = ()

class RoundAdmin(admin.ModelAdmin):
	list_display = ('round_number',)

class GameAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ['name']}

class TeamRoundInline(admin.StackedInline):
    model = TeamRound
    extra = 0

class MatchAdmin(admin.ModelAdmin):
    inlines = [TeamRoundInline,]
    list_display = ('game', 'game_mode', 'player_per_team')
    list_filter = ('game',)

admin.site.register(Team, TeamAdmin)
admin.site.register(Round, RoundAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Match, MatchAdmin)