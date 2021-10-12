from django import forms
from .models import Candidate, Car, ChatMessage


class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        exclude = ['user']


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        exclude = ['name', 'owner', 'reserved', 'to_event']


class CarEditForm(forms.ModelForm):
    class Meta:
        model = Car
        exclude = ['name', 'owner', 'free_chair', 'to_event']


class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ('comment',)