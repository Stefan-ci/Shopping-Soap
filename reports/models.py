from django.db import models

class Expenses(models.Model):
	amount = models.IntegerField(null=True, blank=True, 
		verbose_name="Valeur des dépenses")
	expense_type = models.CharField(max_length=200, 
		verbose_name="Type de dépense")
	reason = models.TextField(verbose_name="Pourquoi ces dépenses ?")
	date = models.DateTimeField(auto_now_add=True, verbose_name='Date')


	class Meta:
		ordering = ['amount', 'expense_type', 'date']
		verbose_name = 'Dépense'
		verbose_name_plural = 'Dépenses'

	def __str__(self):
		return str(self.amount)




class Sales(models.Model):
	amount = models.IntegerField(null=True, blank=True, editable=False,
        verbose_name="Valeur de la vente")
	sale_type = models.CharField(max_length=200, editable=False,
        verbose_name="Type de vente")
	reason = models.TextField(verbose_name="Raisons des ventes")
	date = models.DateTimeField(auto_now_add=True, verbose_name='Date')

	class Meta:
		ordering = ['amount', 'sale_type', 'date']
		get_latest_by = ('date')
		verbose_name = 'Vente'
		verbose_name_plural = 'Vente'

	def __str__(self):
		return str(self.amount)

