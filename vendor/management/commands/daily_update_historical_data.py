from django.core.management.base import BaseCommand
from django.utils import timezone

from vendor.models import HistoricalPerformance, Vendor


class Command(BaseCommand):
    help = "Update historical data for vendors"

    def handle(self, *args, **options):
        # Retrieve all vendors
        vendors = Vendor.objects.all()

        # Iterate through each vendor
        for vendor in vendors:
            # Create historical data record
            historical_data = HistoricalPerformance(
                vendor=vendor,
                date=timezone.now(),
                on_time_delivery_rate=vendor.on_time_delivery_rate,
                quality_rating_avg=vendor.quality_rating_avg,
                average_response_time=vendor.average_response_time,
                fulfillment_rate=vendor.fulfillment_rate,
            )
            historical_data.save()

        self.stdout.write(
            self.style.SUCCESS("Successfully updated historical data for vendors")
        )
