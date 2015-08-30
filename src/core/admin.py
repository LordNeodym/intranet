from django.contrib import admin
from django.db import models
from django.forms import TextInput, Textarea

from core.models import IntranetMeta, Game, Match, Round, Team, Rules, RulesInline, MatchRulesInline


class IntranetMetaAdmin(admin.ModelAdmin):
	pass

class RulesInlineAdmin(admin.StackedInline):	
	model = RulesInline
	extra = 0
	formfield_overrides = {
    	models.TextField: {'widget': Textarea(attrs={'rows':2, 'cols':60})},
    }

class RulesAdmin(admin.ModelAdmin):
	inlines = [RulesInlineAdmin,]

class GameAdmin(admin.ModelAdmin):
	list_display = ('name',)

class RoundAdmin(admin.ModelAdmin):
    list_display = ('round_number', 'team1', 'team2')

class TeamAdmin(admin.ModelAdmin):
	filter_horizontal = ('user',)

class MatchRuleInlineAdmin(admin.TabularInline):
	model = MatchRulesInline
	extra = 0
	formfield_overrides = {
    	models.TextField: {'widget': Textarea(attrs={'rows':2, 'cols':60})},
    }

class MatchAdmin(admin.ModelAdmin):
    list_display = ('game', 'game_mode', 'player_per_team')
    list_filter = ('game',)
    filter_horizontal = ('user',)
    inlines = [MatchRuleInlineAdmin,]
    formfield_overrides = {
    	models.TextField: {'widget': Textarea(attrs={'rows':3, 'cols':40})},
    }


admin.site.register(IntranetMeta, IntranetMetaAdmin)
admin.site.register(Rules, RulesAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(Round, RoundAdmin)