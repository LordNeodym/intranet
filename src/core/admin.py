from django.contrib import admin
from core.models import Game, Match, Round, Team


class GameAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ['name']}

class RoundInline(admin.TabularInline):
    model = Round
    fk_name = 'team1'
    extra = 0

class TeamAdmin(admin.ModelAdmin):
	inlines = [RoundInline,]
	#list_display = ('getTeam',)

class MatchAdmin(admin.ModelAdmin):
    list_display = ('game', 'game_mode', 'player_per_team')
    list_filter = ('game',)
    filter_horizontal = ('user',)


admin.site.register(Team, TeamAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Match, MatchAdmin)