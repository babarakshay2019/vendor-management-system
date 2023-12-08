from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Vendor
from .serializer import (
    VendorGetSerializer,
    VendorPostSerializer,
    VendorPutSerializer,
    VendorPerformanceSerializer,
)
from .permissions import IsCreationOrIsAuthenticated

class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer = VendorGetSerializer
    permission_classes = [IsCreationOrIsAuthenticated]

    serializer_classes = {
        "POST": VendorPostSerializer,
        "PUT": VendorPutSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(self.request.method, self.serializer)


    def create(self, request, *args, **kwargs):
        vendor_serializer = self.get_serializer(data=request.data)

        if vendor_serializer.is_valid():
            vendor = vendor_serializer.save()
            return Response(
                self.serializer(vendor).data, status=status.HTTP_201_CREATED
            )
        return Response(vendor_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=True, methods=["get"], url_path="performance")
    def get_performance_metrics(self, request, pk):
        vendor = self.get_object()
        serializer = VendorPerformanceSerializer(vendor)
        return Response(serializer.data)
