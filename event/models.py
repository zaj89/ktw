from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator


class Event(models.Model):
    name = models.CharField(max_length=30, default='Katolickie Warsztaty Taneczne', verbose_name='Nazwa wydarzenia')
    edition = models.SmallIntegerField(verbose_name='Edycja')
    city = models.CharField(max_length=30, verbose_name='Miasto')
    date = models.DateField(verbose_name='Data wydarzenia', default=timezone.now)
    description = models.TextField(verbose_name="Opis")
    poster = models.ImageField(blank=True, upload_to='posters/%Y/%m/%d', verbose_name='Plakat', default='default/background.png')
    users = models.ManyToManyField(User, verbose_name='Uczestnicy zweryfikowani', related_name='verified', blank=True)
    declarations = models.ManyToManyField(User, verbose_name='Deklaracje udziału', related_name='declared', blank=True)
    users_limit = models.SmallIntegerField(verbose_name='Limit uczestników', blank=False, null=False, default=16)
    bank_name = models.CharField(max_length=30, verbose_name='Nazwa Banku')
    bank_nr = models.CharField(max_length=24, verbose_name='Numer konta', default='')
    reg = (
        ('Otwarta', 'Otwarta'),
        ('Zamknięta', 'Zamknięta'),
    )
    registration = models.CharField(max_length=20, choices=reg, default=reg[0][1], verbose_name='Rejestracja')
    arch = (
        ('Nie', 'Nie'),
        ('Tak', 'Tak'),
    )
    archives = models.CharField(max_length=20, choices=arch, default=arch[0][0], verbose_name='Przenieś do archiwum')

    def Liczba_Uczestników(self):
        return str(len(self.users.all()))

    def limit_wyczerpany(self):
        if (len(self.declarations.all()) + len(self.users.all())) >= self.users_limit:
            print((len(self.declarations.all()) + len(self.users.all())) >= self.users_limit)
            return True
        else:
            print((len(self.declarations.all()) + len(self.users.all())) >= self.users_limit)
            return False

    def __str__(self):
        return self.name + " " + str(self.edition)


class Candidate(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    types = (
        ('Tylko na imprezie integracyjnej od 21:00 do 24:00 (cena 39 zł)',
         'Tylko na imprezie integracyjnej od 21:00 do 24:00 (cena 39 zł)'),
        ('W całodniowych warsztatach od 09:00 do 24:00 (cena 149 zł)',
         'W całodniowych warsztatach od 09:00 do 24:00 (cena 149 zł)'),
    )
    type = models.CharField(max_length=100, choices=types, verbose_name='Chcę uczestniczyć', default=types[0][0])
    question1 = models.TextField(max_length=300, verbose_name='Skąd dowiedziała się Pani/Pan o Warsztatach (znajomi, jeśli FB to jaka nazwa grupy)')
    question2 = models.TextField(max_length=300, verbose_name='Miasto, z którego będzie Pan/Pani wyruszać na warsztaty')
    question3 = models.TextField(max_length=300, verbose_name='Jeśli jedzie Pani/Pan autem, to przez jakie miasta i czy Pani/Pan miałaby/łby wolne miejsca?')
    question4 = models.TextField(max_length=300, verbose_name='Czy ma Pani/Pan jakieś doświadczenie taneczne? Jeśli tak, proszę napisać, czy uczestniczył/a Pani/Pan w kursach tańcach, np. poziom P0, P1, P2, jeśli tak to jakich? Czy posiada Pani/Pan klasy taneczne? Czy zaczyna Pani/Pan absolutnie od podstaw? Proszę podać, do jakich szkół tańca Pani/Pan uczęszczał/a oraz staż tańca.')
    question5 = models.TextField(max_length=300, verbose_name='Czy wierzy Pani/Pan w Boga i jest Pani/Pan praktykującym katolikiem?')
    question6 = models.TextField(max_length=300, verbose_name='Czy należy Pan/Pani do jakiejś wspólnoty? (Jeśli tak, proszę podać nazwę i miasto, w którym odbywają się spotkania.)')
    question7 = models.TextField(max_length=300, verbose_name='Czy uczestniczył/a Pani/Pan w rekolekcjach? Jeśli tak to jakich?')
    question8 = models.TextField(max_length=300, verbose_name='Czy gra Pani / Pan śpiewa lub gra na jakimś instrumencie (gitara, skrzypce etc)? ')

    def __str__(self):
        return "Formularz użytkownika {} dla wydarzenia {}".format(self.user, self.event.name)


class Car(models.Model):
    name = models.CharField(max_length=30, default='Auto', verbose_name='Nazwa')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Właściciel')
    free_chair = models.SmallIntegerField(verbose_name='liczba wolnych miejsc')
    reserved = models.ManyToManyField(User, related_name='rezerwacja', blank=True, verbose_name='Rezerwacja')
    to_event = models.ForeignKey(Event, verbose_name='Wydarzenie', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name) + ' ' + str(self.owner)


class EventNews(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    title = models.CharField(max_length=150, verbose_name='Tytuł')
    text = models.TextField(verbose_name='Treść')
    created = models.DateField(verbose_name='Data utworzenia', auto_now_add=True)
    publicated = models.DateField(verbose_name='Data opublikowania', auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.title


class ChatMessage(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=300, verbose_name='Wiadomość')
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.event.name + ' | ' + self.comment


class ChatMessageToAdmin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usermessage')
    comment = models.TextField(max_length=300, verbose_name='Wiadomość')
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='adminmessage', null=True)
    noreaded = models.BooleanField(verbose_name='Nieprzeczytane', default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return str(self.user.first_name) + ' | ' + str(self.comment)


class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    body = models.TextField(max_length=300, verbose_name='Wiadomość')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Wiadomość wysłana przez{}'.format(self.user.username)


class CarChat(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='car_chat')
    users = models.ManyToManyField(User, related_name='car_users')

    def __str__(self):
        return 'Chat auta {}'.format(self.car.owner.first_name)


class CarChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='caruser')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='carmessage')
    comment = models.TextField(max_length=300, verbose_name='Wiadomość')
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)
