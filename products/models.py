import uuid
from django.db import models
from django.urls import reverse
from hitcount.models import HitCount
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation

STOCK_CHOICES = (
    ('En rupture de stock', 'En rupture de stock'),
    ('Disponible', 'Disponible')
)


TYPE_CHOICES = (
    ('all', 'Tout'),
    ('women', 'Femmes'),
    ('men', 'Hommes'),
    ('children', 'Enfants')
)




class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, max_length=400)
    is_public = models.BooleanField(default=True)
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name', 'added_on']
        verbose_name = 'Catégorie'
        verbose_name_plural = 'Catégorie'

    def __str__(self):
        return str(self.name)
    
    def get_absolute_url(self):
        return reverse('item-category', kwargs={
            'category': self.slug
        })
    
    




class Soap(models.Model):
    hit_count_generic = GenericRelation(HitCount, 
        object_id_field='object_pk',
        related_query_name='hit_count_generic_relation'
    )
    added_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True,
        verbose_name="Ajouter par")
    last_update_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True,
        verbose_name="Dernièrement modifié par", related_name='updated_by')
    name = models.CharField(max_length=255, verbose_name="Nom de l'article")
    subtitle = models.CharField(max_length=255, verbose_name="Sous-titre de l'article", null=True, blank=True)
    slug = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    description = models.TextField(verbose_name="Description de l'article")
    picture = models.ImageField(
        upload_to='images/products/%Y/%m/',
        help_text="Photo/image de l'article à ajouter",
        verbose_name="Image principale")
    tags = TaggableManager()
    picture_2 = models.ImageField(
        null=True,
        blank=True,
        upload_to='images/products/secondaire/%Y/%m/',
        help_text="2e photo/image de l'article à ajouter si besoin",
        verbose_name="Deuxième image")
    picture_3 = models.ImageField(
        null=True,
        blank=True,
        upload_to='images/products/tertiaire/%Y/%m/',
        help_text="3e photo/image de l'article à ajouter si besoin",
        verbose_name="Troisième image")
    price = models.PositiveIntegerField(verbose_name="Prix de l'article",
        help_text="Ne pas inclure la monaie (FCFA)")
    discount_price = models.PositiveIntegerField(blank=True, null=True,
        help_text='Doit être inférieur au prix normal',
        verbose_name="Prix de réduction (rabais)")
    category = models.ForeignKey('Category', on_delete=models.DO_NOTHING,
        verbose_name="Catégorie de l'article")
    type = models.CharField(max_length=12, default="all", blank=True, null=True,
        choices=TYPE_CHOICES, verbose_name="Type de personne")
    shipping_duration = models.IntegerField(default=1, verbose_name="Délai de livraison (Jours)")

    is_popular = models.BooleanField(default=False, verbose_name="Populaire ?")
    is_available = models.CharField(max_length=20, default="Disponible",
        choices=STOCK_CHOICES, verbose_name="Disponibilité")
    is_public = models.BooleanField(default=True, 
        verbose_name="Visible par le public ?")
    is_deleted = models.BooleanField(default=False, 
        verbose_name="Supprimé ?")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Date d'ajout")
    update_date = models.DateTimeField(null=True, blank=True,
        verbose_name="Date de la dernière modification")
    delete_date = models.DateTimeField(null=True, blank=True,
        verbose_name="Date de suppression")
    recover_date = models.DateTimeField(null=True, blank=True,
        verbose_name="Date de restauration")

    full_description = models.TextField(null=True, blank=True,
        help_text="Pas du tout obligatoire",
        verbose_name="Description extremement détaillée")


    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'
        ordering = ['price', 'is_popular', 'is_public', 'date']

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('item-detail', kwargs={
            "slug" : self.slug,
        })

    def get_add_to_cart_url(self):
        return reverse("add-item-to-cart", kwargs={
            "slug" : self.slug,
        })

    def get_remove_from_cart_url(self):
        return reverse("remove-from-cart", kwargs={
            "slug" : self.slug,
        })
    
    def get_add_to_favorites(self):
        return reverse("add-to-favorites", kwargs={"slug":self.slug})
    
    def get_remove_from_favorites(self):
        return reverse("remove-from-favorites", kwargs={"slug":self.slug})
    
    def other_pictures(self):
        imgs = []
        if self.picture_2:
            imgs.append(self.picture_2.url)
        if self.picture_3:
            imgs.append(self.picture_3.url)
        return imgs

    def get_price(self):
        if self.discount_price and self.discount_price != 0:
            if self.discount_price >= self.price:
                return self.price
            return self.price - self.discount_price
        return self.price
    
    def get_saved_amount(self):
        if self.discount_price and self.discount_price != 0:
            return self.price - self.discount_price
        return 0

    def get_discount_percent(self):
        if self.discount_price and self.discount_price != 0:
            if self.discount_price >= self.price:
                return 0
            dis = float((self.discount_price * 100) / self.price)
            return int(dis)
        return 0

    @property
    def filter_by_category(self):
        return Soap.objects.filter(
            is_public=True, is_deleted=False,
            category=self.category
        )

