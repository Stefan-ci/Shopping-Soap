from django.db import models


class Newsletter(models.Model):
    email = models.EmailField(unique=True, verbose_name="Email")
    is_subscribed = models.BooleanField(default=True, verbose_name="abonné(e)")
    is_deleted = models.BooleanField(default=False, verbose_name="Supprimé")
    date = models.DateTimeField(auto_now_add=True, verbose_name='Date')

    class Meta:
        ordering = ['email', 'date']

    def __str__(self):
        return str(self.email)
