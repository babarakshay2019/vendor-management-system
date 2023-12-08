from django.db.models.signals import post_save
from django.dispatch import receiver

from order.models import PurchaseOrder


@receiver(post_save, sender=PurchaseOrder)
def update_vendor_metrics(sender, instance, **kwargs):
    if instance.vendor:
        instance.vendor.update_metrics()
