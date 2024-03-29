# Generated by Django 3.2.7 on 2021-10-11 16:45

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message="Numer telefonu musi być podany w formacie: '+999999999'.", regex='^\\+?1?\\d{9,15}$')], verbose_name='Numer Telefonu')),
                ('city', models.CharField(default='Poznań', max_length=30, verbose_name='Miasto')),
                ('gender', models.CharField(choices=[('Mężczyzna', 'Mężczyzna'), ('Kobieta', 'Kobieta')], default='Mężczyzna', max_length=20, verbose_name='Płeć')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
