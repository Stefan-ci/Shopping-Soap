from django.db import models
from orders.models import Order
from django.contrib.auth.models import User


class Refund(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, 
        blank=True, verbose_name="Utilisateur")
    name = models.CharField(max_length=100, verbose_name="Nom", null=True, 
        blank=True)
    order = models.OneToOneField(Order, on_delete=models.DO_NOTHING, 
        verbose_name="Commande")
    reason = models.TextField(verbose_name="Les raisons")
    accepted = models.BooleanField(default=False, verbose_name="Requête acceptée")
    refused = models.BooleanField(default=False, verbose_name="Réfusée")
    paid = models.BooleanField(default=False, verbose_name="Remboursée")
    email = models.EmailField(verbose_name="Adresse mail du demandeur")
    date = models.DateTimeField(auto_now_add=True, verbose_name='Date')

    class Meta:
        ordering = ['paid', 'accepted', 'date', 'user']
        verbose_name = "Requête de remboursement"
        verbose_name_plural = "Requêtes de remboursement"

    def __str__(self):
        return str(self.email)
