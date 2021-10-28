from django.contrib import admin
from .models import Event, Candidate, Car, EventNews, ChatMessage, CarChat, CarChatMessage


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('name', 'free_chair')


@admin.register(EventNews)
class EventNewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'active', 'publicated')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'edition', 'Liczba_Uczestników')


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('user', 'type')


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'comment', 'created', 'active')

admin.site.register(CarChat)