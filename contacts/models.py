from django.db import models
from django.contrib.auth.models import User


class Contact(models.Model):
	name = models.CharField(max_length=150, verbose_name="Nom")
	email = models.EmailField(verbose_name="Email")
	subject = models.CharField(max_length=100, verbose_name="Sujet")
	message = models.TextField(verbose_name="Message")
	date = models.DateTimeField(auto_now_add=True, verbose_name='Date')
	is_answered = models.BooleanField(default=False, verbose_name="Répondu")
	unread = models.BooleanField(default=True, verbose_name="Non lu")
	deleted = models.BooleanField(default=False, verbose_name="Supprimé")

	class Meta:
		ordering = ['name', 'email', 'subject', 'date']
		verbose_name = "Message reçu"
		verbose_name_plural = "Messages reçus"

	def __str__(self):
		if self.email:
			return str(self.email)
		return str(self.name)
