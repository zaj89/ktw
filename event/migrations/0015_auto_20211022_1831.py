# Generated by Django 3.2.7 on 2021-10-22 18:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0014_event_bank_nr'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='bank_name',
            field=models.CharField(default='PKO BP', max_length=30, verbose_name='Nazwa Banku'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='event',
            name='bank_nr',
            field=models.BigIntegerField(validators=[django.core.validators.MaxValueValidator(9999999999999999), django.core.validators.MinValueValidator(1)], verbose_name='Numer konta'),
        ),
    ]
