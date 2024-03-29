# Generated by Django 4.0.3 on 2022-03-15 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Nom')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('subject', models.CharField(max_length=100, verbose_name='Sujet')),
                ('message', models.TextField(verbose_name='Message')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Date')),
                ('is_answered', models.BooleanField(default=False, verbose_name='Répondu')),
                ('unread', models.BooleanField(default=True, verbose_name='Non lu')),
                ('deleted', models.BooleanField(default=False, verbose_name='Supprimé')),
            ],
            options={
                'verbose_name': 'Message reçu',
                'verbose_name_plural': 'Messages reçus',
                'ordering': ['name', 'email', 'subject', 'date'],
            },
        ),
    ]
