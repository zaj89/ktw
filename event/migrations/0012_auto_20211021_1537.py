# Generated by Django 3.2.7 on 2021-10-21 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0011_alter_candidate_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventnews',
            name='created',
            field=models.DateField(auto_now_add=True, verbose_name='Data utworzenia'),
        ),
        migrations.AlterField(
            model_name='eventnews',
            name='publicated',
            field=models.DateField(auto_now_add=True, verbose_name='Data opublikowania'),
        ),
    ]
