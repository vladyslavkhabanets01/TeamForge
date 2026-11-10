from django.contrib import admin
from .models import LFGPost, Event


@admin.register(LFGPost)
class LFGPostAdmin(admin.ModelAdmin):
    list_display = ['author', 'game', 'role', 'rank', 'is_active', 'created_at']
    list_filter = ['game', 'role', 'rank', 'is_active']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'game', 'event_date', 'max_players']
    list_filter = ['game']
    filter_horizontal = ['participants']
