import uuid
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField





class Promotion(models.Model):
    title = models.CharField(max_length=100, verbose_name="Nom de la promotion")
    description = RichTextUploadingField(verbose_name="Détails de la promotion")
    start_date = models.DateTimeField(verbose_name="Début de la promotion")
    end_date = models.DateTimeField(verbose_name="Fin de la promotion")
    banner = models.ImageField(upload_to="images/promotions/%Y/%m/", verbose_name="Bannière")
    added_on = models.DateTimeField(auto_now_add=True, verbose_name="Date d'ajout")
    slug = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    is_public = models.BooleanField(default=True, verbose_name="Public ?")
    has_expired = models.BooleanField(default=False, verbose_name="A expiré")
    
    class Meta:
        ordering = []
        verbose_name = "Promotion"
        verbose_name_plural = "Promotions"
    
    
    def __str__(self):
        return f"{self.title} du {self.start_date} au {self.end_date}"

