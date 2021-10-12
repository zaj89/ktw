from django.shortcuts import render
from event.models import Event


def index(request):
    events = Event.objects.all()
    return render(request, 'index.html', {'events': events})


def panel_admin(request):
    events = Event.objects.all()
    return render(request, 'account/panel_admin.html', {'events': events})

