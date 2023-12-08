from datetime import timedelta

import factory
from django.contrib.auth.models import User
from django.db.models import Max
from django.utils import timezone

from order.models import PurchaseOrder
from vendor.models import Vendor


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("user_name")
    password = factory.Faker("password")
    email = factory.Faker("email")


class VendorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Vendor

    user = factory.SubFactory(UserFactory)
    name = factory.Faker("company")
    contact_details = factory.Faker("text", max_nb_chars=200)
    address = factory.Faker("text", max_nb_chars=100)
    vendor_code = factory.Faker("uuid4")


class PurchaseOrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PurchaseOrder

    vendor = factory.SubFactory(VendorFactory)
    order_date = factory.LazyFunction(timezone.now)
    delivery_date = factory.LazyFunction(lambda: timezone.now() + timedelta(days=7))
    items = {"mobile": "motorola"}
    quantity = 1
    status = "pending"
    quality_rating = factory.Faker("pyfloat", min_value=0, max_value=5, right_digits=2)
    issue_date = factory.LazyFunction(timezone.now)
    acknowledgment_date = None

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """
        Override default _create to generate a unique PO number.
        """
        po_number = None
        while (
            po_number is None
            or model_class.objects.filter(po_number=po_number).exists()
        ):
            latest_po = model_class.objects.aggregate(Max("id"))
            latest_po_id = latest_po.get("id__max", 0)
            new_number = latest_po_id + 1 if latest_po_id is not None else 1
            po_number = f"PO{new_number}"

        kwargs["po_number"] = po_number
        return super()._create(model_class, *args, **kwargs)
