from django.shortcuts import render
from django.urls import reverse

from .models import Event, Car, EventNews, ChatMessage, ChatMessageToAdmin, CarChatMessage, CarChat
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from .models import Candidate
from .forms import CandidateForm, CarForm, CarEditForm, ChatMessageForm, ChatMessageToAdminForm, CarChatMessageForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.template.defaulttags import register
from django.contrib import messages
from django.http import HttpResponseRedirect


@register.filter
def get_value(dictionary, key):
    return dictionary.get(key)


@register.filter
def plus(one, two):
    return one + two


@register.filter
def bank_number(number):
    number_new = str(number)[:2] + '-' + str(number)[2:6] + '-' + str(number)[6:10] + '-' + str(number)[10:14] + '-' + str(number)[14:18] + '-' + str(number)[18:22]
    return number_new


@register.filter
def noreaded(messages, user_id):
    noreaded_messages = 0
    for message in messages:
        if message.noreaded == True and user_id == message.user.id:
            noreaded_messages += 1
    return noreaded_messages


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
    candidate = Candidate.objects.filter(user_id=request.user.id)
    price = 0
    events = Event.objects.all()
    cars = Car.objects.all()
    car_exist = 0
    carid = 0

    for car in cars:
        if car.owner.id == request.user.id:
            car_exist = 1
            carid = car.id
            pass
    if request.user not in event.users.all():
        if request.method == 'POST':
            candidate_form = CandidateForm(data=request.POST)
            if candidate_form.is_valid():
                new_declare = candidate_form.save(commit=False)
                new_declare.user = request.user
                new_declare.event = event
                if len(candidate) > 0:
                    candidate.delete()
                else:
                    new_declare.save()
                if new_declare:
                    if new_declare.type == new_declare.types[0][0]:
                        price = 39
                    else:
                        price = 149
                user_add = User.objects.get(id=request.user.id)
                event.declarations.add(user_add)
                event.save()
                candidate_form = CandidateForm()
                messages.success(request, "Deklaracja udziału została wysłana.")
                return render(request, 'account/dashboard.html', {'event': event,
                                                                  'candidate_form': candidate_form,
                                                                  'section': 'dashboard',
                                                                  'events': events,
                                                                  'cars': cars,
                                                                  'car_exist': car_exist,
                                                                  'carid': carid,
                                                                  'candidate': candidate,
                                                                  'price': price
                                                                  })
        else:
            candidate_form = CandidateForm()
            return render(request, 'event_declare.html', {'event': event,
                                                          'candidate_form': candidate_form})
    else:
        return render(request, 'account/dashboard.html', {'event': event,
                                                          'section': 'dashboard',
                                                          'events': events,
                                                          'cars': cars,
                                                          'car_exist': car_exist,
                                                          'carid': carid,
                                                          'candidate': candidate,
                                                          'price': price
                                                          })


@login_required
def car_declare(request, id):
    candidate = Candidate.objects.filter(user_id=request.user.id)
    events = Event.objects.all()
    cars = Car.objects.all()
    car_exist = 0
    carid = 0
    for car in cars:
        if car.owner.id == request.user.id:
            car_exist = 1
            carid = car.id
            pass
    event = Event.objects.get(id=id)
    if request.method == 'POST':
        car_form = CarForm(data=request.POST)
        if car_form.is_valid():
            new_declare = car_form.save(commit=False)
            new_declare.owner = request.user
            new_declare.to_event = event
            new_declare.save()
            new_car_chat = CarChat.objects.create(car=new_declare)
            new_car_chat.users.add(new_declare.owner)
            new_car_chat.save()
            messages.success(request, "Przyjazd autem został zadeklarowany.")
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
                                                              'carid': carid,
                                                              'car_form': car_form,
                                                              'candidate': candidate})
    else:
        car_form = CarForm()
        return render(request, 'car_declare.html', {'section': 'dashboard',
                                                    'events': events,
                                                    'cars': cars,
                                                    'car_exist': car_exist,
                                                    'carid': carid,
                                                    'car_form': car_form})


@login_required
def car_undeclare(request, id):
    candidate = Candidate.objects.filter(user_id=request.user.id)
    Car.objects.filter(id=id).delete()
    messages.success(request, "Zadeklarowane auto zostało wycofane.")
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
                                                      'carid': carid,
                                                      'candidate': candidate})

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
    car_chat = CarChat.objects.get(car=car)
    car_chat.users.add(user)
    car_chat.save()

    messages.success(request, "Zarezerwowano miejsce w aucie {}.".format(car.owner.first_name))
    return render(request, 'set_chair.html', {'cars': cars,
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
    car_chat = CarChat.objects.get(car=car)
    car_chat.users.remove(user)
    car_chat.save()
    messages.success(request, "Zadeklarowane miejsce zostało zwolnione.")
    return render(request, 'set_chair.html', {'cars': cars,
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
def car_panel_passenger(request, id):
    car = Car.objects.get(id=id)
    if request.method == 'POST':
        car_edit_form = CarEditForm(data=request.POST)
        if car_edit_form.is_valid():
            new_declare = car_edit_form.save(commit=False)
            new_declare.save()
            return render(request, 'car_panel_passenger.html', {'car': car,
                                                                'car_edit_form': car_edit_form})
    else:
        car_edit_form = CarEditForm()
        return render(request, 'car_panel_passenger.html', {'car': car,
                                                            'car_edit_form': car_edit_form})


@login_required
def event_undeclare(request, id):
    events = Event.objects.all()
    cars = Car.objects.all()
    car_exist = 0
    carid = 0
    for car in cars:
        if car.owner.id == request.user.id:
            car_exist = 1
            carid = car.id
            pass
    event = Event.objects.get(id=id)
    user_remove = User.objects.get(id=request.user.id)
    event.declarations.remove(user_remove)
    event.save()
    cars = Car.objects.all()
    candidate = Candidate.objects.filter(user_id=request.user.id)
    candidate.delete()
    messages.success(request, "Wycofano deklarację udziału w kursie.")
    return render(request, 'account/dashboard.html', {'section': 'dashboard',
                                                      'events': events,
                                                      'cars': cars,
                                                      'car_exist': car_exist,
                                                      'carid': carid})


@login_required
def event_exit(request, id):
    events = Event.objects.all()
    cars = Car.objects.all()
    car_exist = 0
    carid = 0
    for car in cars:
        if car.owner.id == request.user.id:
            car_exist = 1
            carid = car.id
            pass
    event = Event.objects.get(id=id)
    user_exit = User.objects.get(id=request.user.id)
    event.users.remove(user_exit)
    event.save()

    cars = Car.objects.all()
    if cars:
        for car in cars:
            if car.owner.id == user_exit.id:
                car.delete()

    candidate = Candidate.objects.filter(user_id=request.user.id)
    if candidate:
        candidate.delete()
    messages.success(request, "Zrezygnowano z udziału w kursie.")
    return render(request, 'account/dashboard.html', {'section': 'dashboard',
                                                      'events': events,
                                                      'cars': cars,
                                                      'car_exist': car_exist,
                                                      'carid': carid,
                                                      'candidate': candidate})


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
    messagess = ChatMessage.objects.filter(active=True, event_id=id).order_by('created')
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
            messages.success(request, "Wiadomość została wysłana.")
            return HttpResponseRedirect(".")
    else:
        message_form = ChatMessageForm()
    return render(request, 'chat.html', {'event': event,
                                         'messagess': messagess,
                                         'message_form': message_form
                                         })


def chat_car_all_message(request, car_id):
    messagess = CarChatMessage.objects.filter(active=True, car_id=car_id).order_by('created')
    car_chat = CarChat.objects.get(car_id=car_id)
    car = Car.objects.get(id=car_id)
    user = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        message_form = CarChatMessageForm(data=request.POST)
        if message_form.is_valid():
            new_message = message_form.save(commit=False)
            new_message.car = car
            new_message.user = user
            new_message.save()
            message_form = CarChatMessageForm()
            messages.success(request, "Wiadomość została wysłana.")
            return HttpResponseRedirect("chat")
    else:
        message_form = CarChatMessageForm()
    return render(request, 'car_chat.html', {'car_chat': car_chat,
                                             'messagess': messagess,
                                             'message_form': message_form
                                             })


def chat_event_10_messages(request, id):
    messagess = ChatMessage.objects.filter(active=True, event_id=id).order_by('-created')[:10:-1]
    messagess_all = ChatMessage.objects.filter(active=True, event_id=id).order_by('-created')
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
            messages.success(request, "Wiadomość została wysłana.")
            return HttpResponseRedirect(".")
    else:
        message_form = ChatMessageForm()
    return render(request, 'chat10.html', {'event': event,
                                         'messagess': messagess,
                                         'messagess_all': messagess_all,
                                         'message_form': message_form
                                         })


def chat_with_admin(request, id):
    messagess = ChatMessageToAdmin.objects.filter(active=True, user_id=id).order_by('-created')
    user = User.objects.get(id=id)
    if request.method == 'POST':
        message_form = ChatMessageToAdminForm(data=request.POST)
        if message_form.is_valid():
            new_message = message_form.save(commit=False)
            new_message.user = user
            new_message.save()
            message_form = ChatMessageToAdminForm()
            messages.success(request, "Twój wiadomość została wysłana.")
            return HttpResponseRedirect(".")
    else:
        message_form = ChatMessageToAdminForm()
    return render(request, 'chat_with_admin.html', {'messagess': messagess,
                                                    'message_form': message_form
                                                    })


def chat_with_admin_del_mess(request, user_id, mes_id):
    messagess = ChatMessageToAdmin.objects.filter(active=True, user_id=user_id).order_by('-created')
    message_to_remove = messagess.get(id=mes_id)
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        message_form = ChatMessageToAdminForm(data=request.POST)
        if message_form.is_valid():
            new_message = message_form.save(commit=False)
            new_message.user = user
            new_message.save()
            message_form = ChatMessageToAdminForm()
            messages.success(request, "Twój wiadomość została wysłana.")

    else:
        message_form = ChatMessageToAdminForm()
        message_to_remove.delete()
        messages.success(request, "Wiadomość z chatu została skasowana.")
    return render(request, 'chat_with_admin.html', {'messagess': messagess,
                                                    'message_form': message_form,
                                                    'user_id': user_id
                                                    })


def admin_with_user(request, id):
    messagess = ChatMessageToAdmin.objects.filter(active=True, user_id=id).order_by('-created')
    user = User.objects.get(id=id)
    admin = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        message_form = ChatMessageToAdminForm(data=request.POST)
        if message_form.is_valid():
            new_message = message_form.save(commit=False)
            new_message.user = user
            new_message.admin = admin
            new_message.noreaded = False
            new_message.save()
            message_form = ChatMessageToAdminForm()
            messages.success(request, "Wysłano wiadomość chat.")
            return HttpResponseRedirect(".")
    else:
        message_form = ChatMessageToAdminForm()
        if messagess:
            for messag in messagess:
                messag.noreaded = False
                messag.save()
    return render(request, 'chat_admin_with_user.html', {'messagess': messagess,
                                                         'message_form': message_form,
                                                         'user': user
                                                         })


def admin_chat_event_del_message(request, event_id, message_id_to_del):
    messagess = ChatMessage.objects.filter(active=True, event_id=event_id).order_by('-created')
    event = Event.objects.get(id=event_id)
    user = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        message_form = ChatMessageForm(data=request.POST)
        if message_form.is_valid():
            new_message = message_form.save(commit=False)
            new_message.event = event
            new_message.user = user
            new_message.save()
            message_form = ChatMessageForm()

    else:
        message_form = ChatMessageForm()
        message_to_del = messagess.filter(id=message_id_to_del)
        message_to_del.delete()
        messages.success(request, "Wiadomość z chatu została skasowana.")
    return render(request, 'chat.html', {'event': event,
                                         'messagess': messagess,
                                         'message_form': message_form
                                         })


def admin_chat_priv_del_message(request, user_id, message_id_to_del):
    messagess = ChatMessageToAdmin.objects.filter(active=True, user_id=user_id).order_by('-created')
    user = User.objects.get(id=user_id)
    admin = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        message_form = ChatMessageToAdminForm(data=request.POST)
        if message_form.is_valid():
            new_message = message_form.save(commit=False)
            new_message.user = user
            new_message.admin = admin
            new_message.save()
            message_form = ChatMessageToAdminForm()
    else:
        message_form = ChatMessageToAdminForm()
        message_to_del = messagess.filter(id=message_id_to_del)
        message_to_del.delete()
        messages.success(request, "Wiadomość została skasowana.")
    return render(request, 'chat_admin_with_user.html', {'messages': messagess,
                                                         'message_form': message_form,
                                                         'user': user
                                                         })


def admin_verification_declarations(request, event_id):
    event = Event.objects.get(id=event_id)
    candidates = Candidate.objects.filter(event_id=event_id)
    return render(request, 'admin/verification_declarations.html', {'event': event,
                                                                    'candidates': candidates})


def candidate_acceptance(request, event_id, candidate_id):
    candidates = Candidate.objects.all()
    event = Event.objects.get(id=event_id)
    user_acceptance = User.objects.get(id=candidate_id)
    event.declarations.remove(user_acceptance)
    event.users.add(user_acceptance)
    event.save()
    messages.success(request, "Pozytywnie zweryfikowano kursanta.")
    return render(request, 'admin/event_declarations.html', {'event': event,
                                                             'candidates': candidates})


def reject_candidate(request, event_id, candidate_id):
    candidates = Candidate.objects.all()
    event = Event.objects.get(id=event_id)
    user_acceptance = User.objects.get(id=candidate_id)
    event.declarations.remove(user_acceptance)
    event.save()
    candidates.remove(id=candidate_id)
    messages.success(request, "Negatywnie zweryfikowano kursanta.")
    return render(request, 'admin/verification_declarations.html', {'event': event,
                                                                    'candidates': candidates})
