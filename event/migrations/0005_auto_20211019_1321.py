# Generated by Django 3.2.7 on 2021-10-19 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0004_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmessage',
            name='to_admin',
            field=models.BooleanField(default=False, verbose_name='Wiadomość prywatna'),
        ),
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.TextField(verbose_name='Opis'),
        ),
    ]