from django.contrib import admin

from .models import Game, GameDateRelation, PlatformModel,\
    Tag, TagGameRelation, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'owner')


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = (
        'owner', 'id', 'title',
        'platform', 'finished',
        'created', 'modified')


@admin.register(PlatformModel)
class PlatformModelAdmin(admin.ModelAdmin):
    list_display = ('owner', 'id', 'title')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'title')


@admin.register(TagGameRelation)
class TagGameRelationAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', '_tag', '_game')


@admin.register(GameDateRelation)
class GameDateRelationAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'game', 'date')
