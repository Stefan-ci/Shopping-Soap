# Generated by Django 4.0.3 on 2022-03-20 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_soap_is_available'),
    ]

    operations = [
        migrations.AlterField(
            model_name='soap',
            name='is_available',
            field=models.CharField(choices=[('En rupture de stock', 'En rupture de stock'), ('Disponible', 'Disponible'), ('Supprimé', 'Supprimé')], default=('Disponible', 'Disponible'), max_length=20, verbose_name='Disponibilité'),
        ),
    ]
