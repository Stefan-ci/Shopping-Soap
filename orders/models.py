import io
import qrcode
from django.db import models
from products.models import Soap
from coupons.models import Coupon
from django.contrib.auth.models import User
from address.models import ShippingCity, ShippingCountry
from django.core.files.uploadedfile import InMemoryUploadedFile


class OrderItem(models.Model):
    user = models.ForeignKey(User, null=True, blank=True,
        on_delete=models.CASCADE, verbose_name="Utilisateur")
    ordered = models.BooleanField(default=False, verbose_name="Commandé ?")
    item = models.ForeignKey(Soap, on_delete=models.DO_NOTHING,
        verbose_name="Savon choisi")
    quantity = models.IntegerField(default=1, verbose_name="Quantité")
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True,
        verbose_name='Date')

    class Meta:
        verbose_name = "Choix de menus"
        verbose_name_plural = "Choix de menus"


    def __str__(self):
        return f"{self.quantity} de {self.item.name}"

    def get_total_item_price(self):
        return self.quantity * self.item.get_price()
    
    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    


    









class Order(models.Model):
    user = models.ForeignKey(User, null=True, blank=True,
        on_delete=models.DO_NOTHING, verbose_name="Utilisateur")
    unique_code = models.CharField(max_length=50, blank=True, null=True, 
        unique=True, verbose_name="Code de la commande")
    items = models.ManyToManyField(OrderItem, 
        verbose_name="Plats choisis")
    
    start_date = models.DateTimeField(auto_now_add=True, 
        verbose_name="Début de commande")
    ordered_date = models.DateTimeField(null=True, blank=True,
        verbose_name="Date de commande (fin)")
    ordered = models.BooleanField(default=False, 
        verbose_name="Commande effectuée ?")
    
    
    
    shipping_email = models.EmailField(blank=True, null=True,
        verbose_name="Email de commande")
    shipping_phonenumber = models.CharField(max_length=100, blank=True, null=True,
        verbose_name="N° tel de livraison")
    shipping_city = models.ForeignKey(ShippingCity, blank=True, null=True,
        verbose_name="Ville de livraison", on_delete=models.SET_NULL)
    shipping_country = models.ForeignKey(ShippingCountry, blank=True, null=True,
        verbose_name="Pays de livraison", on_delete=models.SET_NULL)
    shipping_firstname = models.CharField(max_length=100, blank=True, null=True,
        verbose_name="Nom")
    shipping_lastname = models.CharField(max_length=100, blank=True, null=True,
        verbose_name="Prenom(s)")
    
    
    
    get_shipping_total = models.BigIntegerField(default=0, 
        verbose_name="Frais de livraison")
    coupon = models.ForeignKey(Coupon, on_delete=models.DO_NOTHING, 
        blank=True, null=True)
    
    being_delivered = models.BooleanField(default=False, 
        verbose_name="En cours de livraison")
    received = models.BooleanField(default=False, verbose_name="Livrée")

    refund_requested = models.BooleanField(default=False,
        verbose_name="Requête de remboursement")
    refund_granted = models.BooleanField(default=False,
        verbose_name="Requête de remboursement acceptée")
    
    order_qr_code = models.ImageField(
        null=True,
        blank=True,
        upload_to='images/commandes/qrcodes/%Y/%m/',
        verbose_name="QR Code",
        # editable=False
    )


    class Meta:
        ordering = ['-id', 'unique_code']
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"


    def __str__(self):
        if self.unique_code:
            return str(self.unique_code)
        return str(self.id)


    


    def get_total(self):
        total = self.get_shipping_total
        for order_item in self.items.all():
            total += order_item.get_total_item_price()
        if self.coupon:
            total -= self.coupon.amount
        return total
    
    

    def generate_order_qr_code(self):
        if self.ordered == True:
            order_total = self.get_total()

            qrcode_data = f"""
                Utilisateur: {self.user}
                Identifiant: {self.unique_code}
                Date de commande: {self.ordered_date}
                Total à payer: {order_total} FCFA

                Commande effectuée: {self.ordered}
                Commande livrée: {self.being_delivered}
                Commande reçue: {self.received}
                Requête de remboursement: {self.refund_requested}
                Requête de remboursement acceptée: {self.refund_granted}

                N° de téléphone: {self.shipping_phonenumber}
                Ville de livraison: {self.shipping_city}
                Pays de livraison: {self.shipping_country}
                Email: {self.shipping_email}
            """

            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )

            qr.add_data(qrcode_data)
            qr.make(fit=True)

            img = qr.make_image()
            buffer = io.BytesIO()
            img.save(buffer)
            contents = buffer.getvalue()

            filename = f"Commande-{self.unique_code}.png"
            filebuffer = InMemoryUploadedFile(
                buffer, None, filename, 'image/png', contents, None
            )
            self.order_qr_code.save(filename, filebuffer)
        else:
            pass
