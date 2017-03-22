from django.contrib import admin

from .models import Game, Tag, TagGameRelation, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'owner')


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = (
        'owner', 'id', 'title',
        'created', 'modified')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'title')


@admin.register(TagGameRelation)
class TagGameRelationAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', '_tag', '_game')
