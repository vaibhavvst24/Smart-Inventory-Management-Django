from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import StockTransaction


@receiver(post_save, sender=StockTransaction)
def update_stock(sender, instance, created, **kwargs):

    if created:

        product = instance.product

        if instance.transaction_type == 'IN':
            product.quantity += instance.quantity

        elif instance.transaction_type == 'OUT':
            product.quantity -= instance.quantity

        product.save()
