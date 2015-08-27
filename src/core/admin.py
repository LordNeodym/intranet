from django.contrib import admin
from core.models import IntranetMeta, Game, Match, Round, Team, Rules, RulesInline


class IntranetMetaAdmin(admin.ModelAdmin):
	pass

class RulesInlineAdmin(admin.StackedInline):	
	model = RulesInline
	extra = 0

class RulesAdmin(admin.ModelAdmin):
	inlines = [RulesInlineAdmin,]

class GameAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ['name']}

class RoundAdmin(admin.ModelAdmin):
    pass

class TeamAdmin(admin.ModelAdmin):
	filter_horizontal = ('user',)

class MatchAdmin(admin.ModelAdmin):
    list_display = ('game', 'game_mode', 'player_per_team')
    list_filter = ('game',)
    filter_horizontal = ('user',)


admin.site.register(IntranetMeta, IntranetMetaAdmin)
admin.site.register(Rules, RulesAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(Round, RoundAdmin)