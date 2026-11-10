from django.contrib import admin
from .models import Game, UserProfile


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'discord', 'steam']
    filter_horizontal = ['games']
