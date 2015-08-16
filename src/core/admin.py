from django.contrib import admin
from core.models import Game, Match, Round


class GameAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ['name']}

class RoundInline(admin.StackedInline):
    model = Round
    extra = 0

class MatchAdmin(admin.ModelAdmin):
    inlines = [RoundInline,]
    list_display = ('game', 'game_mode', 'player_per_team')
    list_filter = ('game',)


admin.site.register(Game, GameAdmin)
admin.site.register(Match, MatchAdmin)