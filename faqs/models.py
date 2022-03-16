from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField




class FAQ(models.Model):
    question = models.CharField(max_length=200, verbose_name="Question")
    answer = RichTextUploadingField(verbose_name="Réponse")
    is_public = models.BooleanField(default=True, verbose_name="Public")
    slug = models.SlugField(unique=True, max_length=400)
    date = models.DateTimeField(auto_now_add=True, verbose_name="Date d'ajout")

    class Meta:
        ordering = ['question', 'date']
        verbose_name = "Qestion/Réponse"
        verbose_name_plural = "Qestions/Réponses"
    
    def __str__(self):
        return str(self.question)
