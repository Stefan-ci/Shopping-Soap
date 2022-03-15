# Generated by Django 4.0.3 on 2022-03-15 23:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, unique=True, verbose_name='Code du coupon')),
                ('reason', models.CharField(blank=True, max_length=500, null=True, verbose_name='Raisons')),
                ('amount', models.PositiveIntegerField(verbose_name='Valeur du coupon')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name="Date d'ajout")),
                ('end_date', models.DateTimeField(verbose_name="Coupon valide jusqu'au")),
                ('is_active', models.BooleanField(default=False, verbose_name='Coupon actif')),
                ('used', models.BooleanField(default=False, verbose_name='Coupon utlisé')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='Utilisateur')),
            ],
        ),
    ]
