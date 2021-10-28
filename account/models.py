from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Numer telefonu musi być podany w formacie: '+999999999'.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True, verbose_name='Numer Telefonu')
    city = models.CharField(max_length=30, verbose_name="Miasto", blank=False, default='Poznań')
    genders = (
        ('Mężczyzna',
         'Mężczyzna'),
        ('Kobieta',
         'Kobieta'),
    )
    gender = models.CharField(max_length=20, choices=genders, verbose_name='Płeć', default=genders[0][1])
    statuss = (
        ('Zwykły',
         'Zwykły'),
        ('Administrator',
         'Administrator'),
    )
    status = models.CharField(max_length=30, choices=statuss, verbose_name='status', default=genders[0][0])

    def __str__(self):
        return 'Profil kursanta {}.'.format(self.user.username)


class Notification(models.Model):
    #Powiadomienia użytkownika
    # 1- Komunikat eventu
    # 2- Wiadomość na Chatcie kursantów
    # 3- Wiadomość na Chatcie z organizatorem
    # 4- Deklaracja udziału odrzucona
    # 5- Deklaracja udziału zaakceptowana
    # 6- Rezerwacja miejca w Twoim aucie
    # 7- Rezygnacja z rezerwacji miejsca w Twoim aucie
    notification_type = models.IntegerField()
    to_user = models.ForeignKey(User, related_name='notification_to', on_delete=models.CASCADE, null=True)
    from_user = models.ForeignKey(User, related_name='notification_from', on_delete=models.CASCADE, null=True)
    comment = models.CharField(max_length=100)
    date = models.DateTimeField(default=timezone.now)
    user_has_seen = models.BooleanField(default=False)
