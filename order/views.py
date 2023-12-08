from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .models import PurchaseOrder
from .serializer import (
    PurchaseOrderGetSerializer,
    PurchaseOrderPostSerializer,
    PurchaseOrderPutSerializer,
)


class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer = PurchaseOrderGetSerializer

    serializer_classes = {
        "POST": PurchaseOrderPostSerializer,
        "PUT": PurchaseOrderPutSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.request.method, self.serializer)

    @action(detail=True, methods=["post"])
    def acknowledge(self, request, pk=None):
        purchase_order = self.get_object()

        # Check if acknowledgment_date is already set
        if purchase_order.acknowledgment_date is not None:
            raise ValidationError("This purchase order has already been acknowledged.")

        # Set the acknowledgment_date to current time
        purchase_order.acknowledgment_date = timezone.now()
        purchase_order.save()

        return Response(self.serializer(purchase_order).data, status=status.HTTP_200_OK)
