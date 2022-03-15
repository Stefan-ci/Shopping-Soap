from django.contrib.auth.models import User
from django.db.models.signals import post_save
#from notifications.signals import notify
from reports.models import Sales, Expenses
from orders.models import Order, OrderItem



def create_sale_report(sender, instance, created, **kwargs):
    if created:
        if instance.ordered == True:
            Sales.objects.create(
                amount=instance.amount,
                sale_type="Vente",
                reason="Nouvelle commande de menu sur le site",
            )
post_save.connect(create_sale_report, sender=Order)



'''
def sales_ping_admins(sender, instance, created, **kwargs):
    if created:
        notify.send(instance, 
            recipient=User.objects.filter(is_superuser=True), 
            verb="Nouvelle vente",
            level='success',

            amount=instance.amount,
            type=instance.sale_type,
            reason=instance.reason,
            date=instance.date
        )
post_save.connect(sales_ping_admins, sender=Sales)




def expenses_ping_admins(sender, instance, created, **kwargs):
    if created:
        notify.send(instance, 
            recipient=User.objects.filter(is_superuser=True), 
            verb="Nouvelle dépense",
            level='error',

            amount=instance.amount,
            type=instance.expense_type,
            reason=instance.reason,
            date=instance.date
        )
post_save.connect(expenses_ping_admins, sender=Expenses)


'''