from django.db import models
from django_countries.fields import CountryField




class ShippingCountry(models.Model):
    country = country = CountryField(default='CI', verbose_name='Pays de livraison',
        unique=True)
    date = models.DateTimeField(auto_now_add=True, verbose_name='Date')
    
    
    class Meta:
        ordering = ['country', 'date']
        verbose_name = "Pays de livraison"
        verbose_name_plural = "Pays de livraison"
    
    def __str__(self):
        return str(self.country.name)
    





    




class ShippingCity(models.Model):
    country = models.ForeignKey(ShippingCountry, on_delete=models.CASCADE, verbose_name='Pays')
    city = models.CharField(max_length=200, verbose_name="Ville de livraison", unique=True)
    date = models.DateTimeField(auto_now_add=True, verbose_name='Date')
    
    class Meta:
        ordering = ['city', 'country', 'date']
        verbose_name = "Ville de livraison"
        verbose_name_plural = "Villes de livraison"
    
    def __str__(self):
        return f"{self.city}"




