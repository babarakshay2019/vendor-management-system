from rest_framework import serializers
from .models import PurchaseOrder

class PurchaseOrderPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = PurchaseOrder
        exclude = ['po_number']

class PurchaseOrderPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        exclude = ['po_number', 'vendor']

class PurchaseOrderGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'