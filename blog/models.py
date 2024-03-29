from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField







class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, verbose_name="Poste")
    name = models.CharField(max_length=50, verbose_name="Nom")
    website = models.CharField(max_length=100, verbose_name="Site internet", null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    content = models.TextField(verbose_name="Commentaire")
    is_public = models.BooleanField(default=True, verbose_name="Public")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Date d'ajout")
    
    
    class Meta:
        ordering = ['-date']
        verbose_name = "Commentaire"
        verbose_name_plural = "Commentaires"
        
        
    def __str__(self):
        return str(self.name)





class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="Titre de la publication")
    picture = models.ImageField(upload_to="images/blog/%Y/%m/", verbose_name="Image")
    slug = models.SlugField(unique=True, max_length=400)
    description = RichTextUploadingField(verbose_name="Réponse")
    tags = TaggableManager()
    is_public = models.BooleanField(default=True, verbose_name="Public")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Date d'ajout")


    class Meta:
        ordering = ['-date', 'title', 'is_public']
        verbose_name = "Publication"
        verbose_name_plural = "Publications"
    
    
    def __str__(self):
        return str(self.title)
    
    def get_absolute_url(self):
        return reverse('blog:post-detail', kwargs={
            "slug" : self.slug,
        })
    
    def blog_comments(self):
        return Comment.objects.filter(post=self, is_public=True)
    
    def blog_comments_count(self):
        return Comment.objects.filter(post=self, is_public=True).count()







