from django.shortcuts import render, get_object_or_404
from event.models import Event, EventNews
from django.contrib.auth.models import User
from event.models import Contact, Candidate, ChatMessageToAdmin
from event.forms import ContactForm, EventForm, EventNewsForm
from django.contrib.auth.decorators import login_required
from account.models import Profile
from account.forms import AdminToUserMailForm
from django.core.mail import send_mail
from django.contrib import messages


def index(request):
    events = Event.objects.all()
    return render(request, 'index.html', {'events': events})


@login_required
def panel_admin(request):
    events = Event.objects.all()
    return render(request, 'admin/panel_admin.html', {'events': events})


@login_required
def admin_users_list(request):
    users = User.objects.all().exclude(id=1)
    profiles = Profile.objects.all().exclude(id=1)
    messagess = ChatMessageToAdmin.objects.all()
    return render(request, 'admin/users.html', {'users': users,
                                                'profiles': profiles,
                                                'messagess': messagess,
                                                })


@login_required
def admin_events_list(request):
    events = Event.objects.all()
    return render(request, 'admin/events.html', {'events': events})


@login_required
def admin_event_detail(request, event_id):
    event = Event.objects.get(id=event_id)
    instance = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event_form = EventForm(request.POST or None, instance=instance)
        if event_form.is_valid():
            new_event = event_form.save(commit=False)
            new_event.save()
            # messages.success(request, "Twój wiadomość została wysłana.")
    else:
        event_form = EventForm(request.POST or None, instance=instance)
    return render(request, 'admin/event.html', {'event': event,
                                                'event_form': event_form
                                                })


@login_required
def admin_event_edit(request, event_id):
    event = Event.objects.get(id=event_id)
    instance = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event_form = EventForm(request.POST or None, instance=instance)
        if event_form.is_valid():
            new_event = event_form.save(commit=False)
            new_event.save()
            messages.success(request, "Zmiany został zapisane.")
    else:
        event_form = EventForm(request.POST or None, instance=instance)
    return render(request, 'admin/event_edit.html', {'event': event,
                                                     'event_form': event_form
                                                     })


@login_required
def admin_event_declarations(request, event_id):
    event = Event.objects.get(id=event_id)
    instance = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event_form = EventForm(request.POST or None, instance=instance)
        if event_form.is_valid():
            new_event = event_form.save(commit=False)
            new_event.save()
            # messages.success(request, "Twój wiadomość została wysłana.")
    else:
        event_form = EventForm(request.POST or None, instance=instance)
    return render(request, 'admin/event_declarations.html', {'event': event,
                                                             'event_form': event_form
                                                             })


@login_required
def admin_event_declarations_form(request, event_id, user_id):
    event = Event.objects.get(id=event_id)
    user = User.objects.get(id=user_id)
    event_form = Candidate.objects.get(user_id=user_id, event_id=event_id)
    return render(request, 'admin/event_declaration_form.html', {'event': event,
                                                                 'user': user,
                                                                 'event_form': event_form
                                                                 })


@login_required
def admin_event_news(request, event_id):
    event = Event.objects.get(id=event_id)
    instance = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event_form = EventForm(request.POST or None, instance=instance)
        if event_form.is_valid():
            new_event = event_form.save(commit=False)
            new_event.save()
            # messages.success(request, "Twój wiadomość została wysłana.")
    else:
        event_form = EventForm(request.POST or None, instance=instance)
    return render(request, 'admin/event_news.html', {'event': event,
                                                     'event_form': event_form
                                                     })


@login_required
def admin_event_news_list(request, event_id):
    event = Event.objects.get(id=event_id)
    news = EventNews.objects.filter(event_id=event_id).order_by('-date')
    if request.method == 'POST':
        event_form = EventNewsForm(request.POST or None)
        if event_form.is_valid():
            new_event = event_form.save(commit=False)
            new_event.event = event
            new_event.save()
            # messages.success(request, "Twój wiadomość została wysłana.")
    else:
        event_form = EventNewsForm()
    return render(request, 'admin/event_news_list.html', {'event': event,
                                                          'event_form': event_form,
                                                          'news': news
                                                          })



@login_required
def admin_event_news_del(request, event_id, news_id):
    event = Event.objects.get(id=event_id)
    news = EventNews.objects.filter(event_id=event_id).order_by('-date')
    new_to_del = news.objects.get(id=news_id)
    if request.method == 'POST':
        event_form = EventNewsForm(request.POST or None)
        if event_form.is_valid():
            new_event = event_form.save(commit=False)
            new_event.event = event
            new_event.save()
            messages.success(request, "Komunikat został skasowany.")
    else:
        event_form = EventNewsForm()
        new_to_del.delete()
    return render(request, 'admin/event_news_list.html', {'event': event,
                                                          'event_form': event_form,
                                                          'news': news
                                                          })


@login_required
def admin_event_news_edit(request, event_id, news_id):
    event = Event.objects.get(id=event_id)
    news = EventNews.objects.filter(event_id=event_id).order_by('-date')
    new_to_edit = news.get(id=news_id)
    if request.method == 'POST':
        event_form = EventNewsForm(request.POST)
        if event_form.is_valid():
            new_event = event_form.save(commit=False)
            new_event.event = event
            new_event.save()
            messages.success(request, "Zapisano zmiany w komunikacie.")
    else:
        event_form = EventNewsForm(instance=new_to_edit)
    return render(request, 'admin/event_news_edit.html', {'event': event,
                                                          'event_form': event_form,
                                                          'news': news
                                                          })


@login_required
def admin_event_news_new(request, event_id):
    event = Event.objects.get(id=event_id)
    if request.method == 'POST':
        event_form = EventNewsForm(request.POST, request.FILES)
        if event_form.is_valid():
            new_event = event_form.save(commit=False)
            new_event.event = event
            new_event.save()
            event_form = EventNewsForm()
            messages.success(request, "Opublikowane nowy komunikat.")
    else:
        event_form = EventNewsForm()
    return render(request, 'admin/event_news_new.html', {'event': event,
                                                         'event_form': event_form,
                                                         })


@login_required
def admin_mails(request):
    mails = Contact.objects.all()
    return render(request, 'admin/mails.html', {'mails': mails})


@login_required
def contact(request):
    user = User.objects.get(id=request.user.id)
    if request.method == "POST":
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            new_contact = contact_form.save(commit=False)
            new_contact.user = user
            new_contact.save()
            return render(request, 'contact.html', {'contact_form': contact_form})
    else:
        contact_form = ContactForm()
        return render(request, 'contact.html', {'contact_form': contact_form})


def admin_email_to_user(request, user_id):
    sent = False
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = AdminToUserMailForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            subject = 'Administrator Katolickich Warsztatów Tanecznych napisał do Ciebie wiadomość.'
            message = 'Treść wiadomości: {}'.format(cd['message'])
            send_mail(subject, message, 'zajac89@o2.pl', ['admin@o2.pl'])
            sent = True
            #messages.success(request, "Wysłano wiadomość do kursanta.")
    else:
        form = AdminToUserMailForm()
    return render(request, 'admin/email_to_user.html', {'form': form,
                                                        'sent': sent,
                                                        'user': user
                                                        })


@login_required
def admin_delete_declaration(request, event_id, user_id):
    event = Event.objects.get(id=event_id)
    instance = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event_form = EventForm(request.POST or None, instance=instance)
        if event_form.is_valid():
            new_event = event_form.save(commit=False)
            new_event.save()
            # messages.success(request, "Twój wiadomość została wysłana.")
    else:
        event_form = EventForm(request.POST or None, instance=instance)
        user_declaration = event.declarations.get(id=user_id)
        user_poll = Candidate.objects.get(user=user_declaration)
        event.declarations.remove(user_declaration)
        event.save()
        user_poll.delete()
    return render(request, 'admin/event.html', {'event': event,
                                                'event_form': event_form
                                                })


@login_required
def admin_delete_user_verified(request, event_id, user_id):
    event = Event.objects.get(id=event_id)
    instance = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event_form = EventForm(request.POST or None, instance=instance)
        if event_form.is_valid():
            new_event = event_form.save(commit=False)
            new_event.save()
            # messages.success(request, "Twój wiadomość została wysłana.")
    else:
        event_form = EventForm(request.POST or None, instance=instance)
        user_verified = event.users.get(id=user_id)
        user_poll = Candidate.objects.get(user=user_verified)
        event.users.remove(user_verified)
        event.save()
        user_poll.delete()
    return render(request, 'admin/event.html', {'event': event,
                                                'event_form': event_form
                                                })