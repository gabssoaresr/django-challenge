from rest_framework import serializers
from .models import Inventory


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        extra_kwargs = {
            'menu_item': {'required': False} 
        }
        fields = ['id', 'menu_item', 'available_quantity']