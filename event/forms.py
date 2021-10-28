from django import forms
from .models import Candidate, Car, ChatMessage, Contact, Event, ChatMessageToAdmin, EventNews, CarChatMessage


class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        exclude = ['user', 'event']


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        exclude = ['name', 'owner', 'reserved', 'to_event']


class CarEditForm(forms.ModelForm):
    class Meta:
        model = Car
        exclude = ['name', 'owner', 'free_chair', 'to_event']


class ChatMessageToAdminForm(forms.ModelForm):
    class Meta:
        model = ChatMessageToAdmin
        fields = ('comment',)


class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ('comment',)


class CarChatMessageForm(forms.ModelForm):
    class Meta:
        model = CarChatMessage
        fields = ('comment',)


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        exclude = ['user', 'created']


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'edition', 'city', 'date', 'description', 'poster', 'users_limit', 'registration', 'archives']


class EventNewsForm(forms.ModelForm):
    class Meta:
        model = EventNews
        exclude = ['event', 'created', 'publicated', 'active']
