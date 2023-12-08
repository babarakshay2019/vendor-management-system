from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Max

from vendor.models import Vendor


class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("canceled", "Canceled"),
    ]

    po_number = models.CharField(max_length=50, unique=True, null=True, blank=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    quality_rating = models.FloatField(
        null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.po_number} - {self.vendor.name}"

    def save(self, *args, **kwargs):
        if not self.po_number:
            latest_po = PurchaseOrder.objects.aggregate(Max("id"))
            latest_po_id = latest_po.get("id__max", 0)
            new_number = latest_po_id + 1 if latest_po_id is not None else 1
            self.po_number = f"PO{new_number}"
        super().save(*args, **kwargs)
