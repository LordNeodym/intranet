from django.contrib import admin
from django.db import models
from django.forms import TextInput, Textarea
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from core.models import IntranetMeta, Game, Match, Round, Team, Rules, RulesInline, VideoCategory, SingleVideo, ImageCategory, SingleImage, UserExtension, MenuOrder, SingleMenuOrder


class UserExtensionInlineAdmin(admin.StackedInline):
    model = UserExtension
    extra = 1

class UserAdmin(UserAdmin):
    inlines = [UserExtensionInlineAdmin,]


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
    list_filter = ('match',)


class TeamAdmin(admin.ModelAdmin):
    filter_horizontal = ('user',)


class MatchAdmin(admin.ModelAdmin):
    list_display = ('game', 'game_mode', 'player_per_team')
    list_filter = ('game',)
    filter_horizontal = ('user',)


class VideoInlineAdmin(admin.TabularInline):
    model = SingleVideo
    extra = 0


class VideoCategoryAdmin(admin.ModelAdmin):
    inlines = [VideoInlineAdmin,]
    ordering = ['description']


class ImageInlineAdmin(admin.TabularInline):
    model = SingleImage
    extra = 0


class ImageCategoryAdmin(admin.ModelAdmin):
    inlines = [ImageInlineAdmin,]
    ordering = ['description']


class MenuOrderAdmin(admin.ModelAdmin):
    list_display = ('description', 'timestamp',)
    ordering = ['-timestamp']


class SingleMenuOrderAdmin(admin.ModelAdmin):
    list_display = ('order', 'name')
    ordering = ['-order', '-name']


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(IntranetMeta, IntranetMetaAdmin)
admin.site.register(Rules, RulesAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(Round, RoundAdmin)
admin.site.register(VideoCategory, VideoCategoryAdmin)
admin.site.register(ImageCategory, ImageCategoryAdmin)
admin.site.register(MenuOrder, MenuOrderAdmin)
admin.site.register(SingleMenuOrder, SingleMenuOrderAdmin)
