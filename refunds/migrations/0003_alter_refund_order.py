# Generated by Django 4.0.3 on 2022-03-20 11:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_order_order_total'),
        ('refunds', '0002_refund_refused_alter_refund_paid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='refund',
            name='order',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='orders.order', verbose_name='Commande'),
        ),
    ]
