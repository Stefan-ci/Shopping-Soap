from django.db import models
from django.contrib.auth.models import User


class Coupon(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, 
        verbose_name="Utilisateur", null=True, blank=True)
    code = models.CharField(max_length=50, verbose_name="Code du coupon",
        unique=True)
    reason = models.CharField(max_length=500, verbose_name="Raisons",
        null=True, blank=True)
    amount = models.PositiveIntegerField(verbose_name="Valeur du coupon")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Date d'ajout")
    end_date = models.DateTimeField(verbose_name="Coupon valide jusqu'au")
    is_active = models.BooleanField(default=False, verbose_name="Coupon actif")
    used = models.BooleanField(default=False, verbose_name="Coupon utlisé")

    def __str__(self):
        return self.code
