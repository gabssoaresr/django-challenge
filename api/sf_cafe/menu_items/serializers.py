from rest_framework import serializers
from .models import MenuItem
from sf_cafe.inventory.serializers import InventorySerializer
from sf_cafe.inventory.models import Inventory


class MenuItemSerializer(serializers.ModelSerializer):
    new_photo = serializers.ImageField(write_only=True)
    inventory = InventorySerializer(read_only=True, many=False)
    
    class Meta:
        model = MenuItem
        fields = [
            'id', 
            'name', 
            'description', 
            'price', 
            'photo_path', 
            'ingredients', 
            'nutritional_information', 
            'inventory',
            'new_photo',
        ]
        read_only_fields = ['photo_path']
        depth = 1

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['price'] = instance.get_price_float() 
        data['photo_path'] = instance.get_photo_path_download_url() 
        return data

    def create(self, validated_data):
        new_photo = validated_data.pop('new_photo', None)

        menu_item = MenuItem(**validated_data)

        if new_photo:
            menu_item.new_photo = new_photo

        menu_item.save()
        
        return menu_item