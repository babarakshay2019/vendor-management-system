from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import PurchaseOrderViewSet

router = DefaultRouter()
router.register(r"purchase_orders", PurchaseOrderViewSet, basename="purchase_orders")

urlpatterns = [
    path("api/", include(router.urls)),
]
