from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator


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