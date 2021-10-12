from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Event, Car, EventNews, ChatMessage
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from .models import Candidate
from .forms import CandidateForm, CarForm, CarEditForm, ChatMessageForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.template.defaulttags import register



@register.filter
def get_value(dictionary, key):
    return dictionary.get(key)


def event_detail(request, id):
    event = Event.objects.get(id=id)
    return render(request, 'event_detail.html', {'event': event})


def event_news(request, id):
    event = Event.objects.get(id=id)
    news = EventNews.objects.filter(event=event)
    return render(request, 'event_news.html', {'event': event,
                                               'news': news})


@login_required
def event_declare(request, id):
    event = Event.objects.get(id=id)
    if request.user not in event.users.all():
        if request.method == 'POST':
            candidate_form = CandidateForm(data=request.POST)
            if candidate_form.is_valid():
                new_declare = candidate_form.save(commit=False)
                new_declare.user = request.user
                new_declare.save()
                user_add = User.objects.get(id=request.user.id)
                event.declarations.add(user_add)
                event.save()
                # messages.success(request, "Twój Komentarz został dodany.")
                return render(request, 'event_declared.html', {'event': event,
                                                               'candidate_form': candidate_form})
        else:
            candidate_form = CandidateForm()
            print('sdfsdfsdfsdf')
            return render(request, 'event_declare.html', {'event': event,
                                                      'candidate_form': candidate_form})
    else:
        print(event.declarations)
        return render(request, 'event_declared.html', {'event': event})


@login_required
def car_declare(request, id):
    event = Event.objects.get(id=id)
    if request.method == 'POST':
        car_form = CarForm(data=request.POST)
        if car_form.is_valid():
            new_declare = car_form.save(commit=False)
            new_declare.owner = request.user
            new_declare.to_event = event
            new_declare.save()
            # messages.success(request, "Twój Komentarz został dodany.")
            return render(request, 'car_declared.html', {'event': event,
                                                         'car_form': car_form})
    else:
        car_form = CarForm()
        return render(request, 'car_declare.html', {'event': event,
                                                    'car_form': car_form})


@login_required
def car_undeclare(request, id):
    Car.objects.filter(id=id).delete()
    # messages.success(request, "Twój Komentarz został dodany.")
    events = Event.objects.all()
    cars = Car.objects.all()
    car_exist = 0
    carid = 0
    for car in cars:
        if car.owner.id == request.user.id:
            car_exist = 1
            carid = car.id
            pass
    return render(request, 'account/dashboard.html', {'section': 'dashboard',
                                                      'events': events,
                                                      'cars': cars,
                                                      'car_exist': car_exist,
                                                      'carid': carid})


@login_required
def set_chair(request, id):
    cars = Car.objects.all()
    event = Event.objects.get(id=id)
    cities = []
    for use in event.users.all():
        cities.append(use.profile.city)
    cities = set(cities)
    return render(request, 'set_chair.html', {'cars': cars,
                                              'event': event,
                                              'cities': cities})


def chair_declare(request, car_id, eventid):
    events = Event.objects.all()
    cars = Car.objects.all()
    car_exist = 0
    carid = 0
    lenregevent = 0
    lendecevent = 0
    for car in cars:
        if car.owner.id == request.user.id:
            car_exist = 1
            carid = car.id
            pass
    event = Event.objects.get(id=eventid)
    cities = []
    for use in event.users.all():
        cities.append(use.profile.city)
    cities = set(cities)
    car = Car.objects.get(id=car_id)
    user = User.objects.get(id=request.user.id)
    car.reserved.add(user)
    car.save()
    return render(request, 'event_info.html', {'cars': cars,
                                                      'event': event,
                                                      'cities': cities,
                                                      'section': 'dashboard',
                                                      'events': events,
                                                      'car_exist': car_exist,
                                                      'carid': carid,
                                                      'lenregevent': lenregevent,
                                                      'lendecevent': lendecevent
                                                      })


def chair_undeclare(request, car_id, eventid):
    events = Event.objects.all()
    cars = Car.objects.all()
    car_exist = 0
    carid = 0
    lenregevent = 0
    lendecevent = 0
    for car in cars:
        if car.owner.id == request.user.id:
            car_exist = 1
            carid = car.id
            pass
    event = Event.objects.get(id=eventid)
    cities = []
    for use in event.users.all():
        cities.append(use.profile.city)
    cities = set(cities)
    car = Car.objects.get(id=car_id)
    user = User.objects.get(id=request.user.id)
    car.reserved.remove(user)
    car.save()
    return render(request, 'event_info.html', {'cars': cars,
                                                      'event': event,
                                                      'cities': cities,
                                                      'section': 'dashboard',
                                                      'events': events,
                                                      'car_exist': car_exist,
                                                      'carid': carid,
                                                      'lenregevent': lenregevent,
                                                      'lendecevent': lendecevent
                                                      })


@login_required
def car_panel(request, id):
    car = Car.objects.get(id=id)
    if request.method == 'POST':
        car_edit_form = CarEditForm(data=request.POST)
        if car_edit_form.is_valid():
            new_declare = car_edit_form.save(commit=False)
            new_declare.save()
            return render(request, 'car_panel.html', {'car': car,
                                                      'car_edit_form': car_edit_form})
    else:
        car_edit_form = CarEditForm()
        return render(request, 'car_panel.html', {'car': car,
                                                  'car_edit_form': car_edit_form})
    return render(request, 'car_panel.html', {})


@login_required
def event_undeclare(request, id):
    event = Event.objects.get(id=id)
    user_remove = User.objects.get(id=request.user.id)
    event.declarations.remove(user_remove)
    event.save()
    return render(request, 'event_undeclared.html', {'event': event})


@login_required
def event_exit(request, id):
    event = Event.objects.get(id=id)
    event_exit = User.objects.get(id=request.user.id)
    event.users.remove(event_exit)
    event.save()
    return render(request, 'event_exit.html', {'event': event})


@login_required
def event_info(request, id):
    event = Event.objects.get(id=id)
    cars = Car.objects.all()
    cities = []
    for use in event.users.all():
        cities.append(use.profile.city)
    cities = set(cities)
    cities_cars_len = {}
    for city in cities:
        car_in_city = 0
        for car in cars:
            if car.owner.profile.city == city:
                car_in_city += 1
            else:
                pass
        cities_cars_len[city] = car_in_city
    return render(request, 'event_info.html', {'event': event,
                                               'cities': cities,
                                               'cars': cars,
                                               'cities_cars_len': cities_cars_len})


def events_list(request):
    events = Event.objects.all()
    return render(request, 'events_list.html', {'events': events})


class CandidateCreate(LoginRequiredMixin, CreateView):
    model = Candidate
    exclude = ['user']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


def chat_event_all_message(request, id):
    messages = ChatMessage.objects.filter(active=True, event_id=id).order_by('-created')
    event = Event.objects.get(id=id)
    user = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        message_form = ChatMessageForm(data=request.POST)
        if message_form.is_valid():
            new_message = message_form.save(commit=False)
            new_message.event = event
            new_message.user = user
            new_message.save()
            message_form = ChatMessageForm()
            #messages.success(request, "Twój wiadomość została wysłana.")

    else:
        message_form = ChatMessageForm()
    return render(request, 'chat.html', {'event': event,
                                         'messages': messages,
                                         'message_form': message_form,
                                         })

