from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg, Max
from django.utils import timezone


class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True, blank=True, null=True)
    on_time_delivery_rate = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)], null=True
    )
    quality_rating_avg = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(5)], null=True
    )
    average_response_time = models.FloatField(
        validators=[MinValueValidator(0)], null=True
    )
    fulfillment_rate = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)], null=True
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.vendor_code:
            latest_vendor = Vendor.objects.aggregate(Max("id"))
            latest_vendor_id = latest_vendor.get("id__max", 0)
            new_number = latest_vendor_id + 1 if latest_vendor_id is not None else 1
            self.vendor_code = f"VID{new_number}"
        super().save(*args, **kwargs)

    def update_metrics(self):
        completed_orders = self.purchaseorder_set.filter(status="completed")

        if not completed_orders.exists():
            return

        self.on_time_delivery_rate = (
            completed_orders.filter(delivery_date__lte=timezone.now()).count()
            / completed_orders.count()
            * 100
        )
        self.quality_rating_avg = (
            completed_orders.aggregate(Avg("quality_rating"))["quality_rating__avg"]
            or 0
        )
        self.average_response_time = self.calculate_response_time(completed_orders)
        self.fulfillment_rate = (
            completed_orders.filter(status="completed").count()
            / self.purchaseorder_set.count()
            * 100
        )

        self.save()

    @staticmethod
    def calculate_response_time(purchase_orders):
        response_times = [
            (po.acknowledgment_date - po.issue_date).total_seconds()
            for po in purchase_orders
        ]
        return sum(response_times) / len(response_times) if response_times else 0


class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    quality_rating_avg = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    average_response_time = models.FloatField(validators=[MinValueValidator(0)])
    fulfillment_rate = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    def __str__(self):
        return f"{self.vendor.name} - {self.date}"
