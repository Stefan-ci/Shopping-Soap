import uuid
from django.db import models
from products.models import Soap
from orders.models import OrderItem, Order
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, 
        verbose_name="Utilisateur")
    phone_number = PhoneNumberField(blank=True, null=True,
        verbose_name="N° de tel")
    unique_token = models.UUIDField(default=uuid.uuid4, unique=True)
    avatar = models.ImageField(null=True, blank=True,
        upload_to='images/profils/avatars/%Y/%m/',
        default="default/user.png",
        verbose_name='Photo de profil')

    signup_lat_long = models.CharField(max_length=50, null=True, blank=True,
        verbose_name="Coordonnées (à l'inscription)")
    signup_hostname = models.CharField(max_length=1000, null=True, blank=True,
        verbose_name="Appareil (à l'inscription)")
    signup_ip = models.CharField( max_length=15, null=True, blank=True,
        verbose_name="Adresse IP (à l'inscription)")
    signup_browser = models.CharField(max_length=1000, null=True, blank=True,
        verbose_name="Navigateur (à l'inscription)")

    last_login_lat_long = models.CharField(max_length=50, null=True, blank=True,
        verbose_name="Coordonnées (connexion)")
    last_login_hostname = models.CharField(max_length=1000, null=True, blank=True,
        verbose_name="Appareil (connexion)")
    last_login_ip = models.CharField(max_length=15, null=True, blank=True,
        verbose_name="Adresse IP (connexion)")
    last_login_browser = models.CharField(max_length=1000, null=True, blank=True,
        verbose_name="Navigateur (connexion)")
    
    favorite_items = models.ManyToManyField(Soap, blank=True, verbose_name="Articles favoris")

    is_dispatcher = models.BooleanField(default=False, verbose_name="Livreur ?")
    is_dev = models.BooleanField(default=False, verbose_name="Dévéloppeur du site")
    date_joined = models.DateTimeField(auto_now_add=True, 
        verbose_name="Date d'inscription")


    class Meta:
        verbose_name = "Profil d'utlisateur"
        verbose_name_plural = "Profil des utlisateurs"

    def __str__(self):
        return f'{self.user.username}'

    def cart_item_count(self):
        return OrderItem.objects.filter(user=self.user, ordered=False).count()

    def cart_items(self):
        return Order.objects.filter(user=self.user, ordered=False)
    
    def count_fav_items(self):
        return self.favorite_items.count()

