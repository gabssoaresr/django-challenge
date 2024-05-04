from rest_framework import serializers
from .models import Order, OrderDetail
from sf_cafe.user.serializers import CustomerSerializer
from sf_cafe.menu_items.serializers import MenuItemSerializer, MenuItem


class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'order_date', 'total_order', 'status', 'payment_method', 'payied_at']
        read_only_fields = ['id', 'order_date', 'total_order', 'payied_at']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['total_order'] = instance.get_total_order_float() 
        return data
    

class OrderDetailSerializer(serializers.ModelSerializer):
    menu_item_id = serializers.IntegerField() 
    order_id = serializers.IntegerField() 
    order = OrderSerializer(read_only=True)
    menu_item = MenuItemSerializer(read_only=True)

    class Meta:
        model = OrderDetail
        fields =  ['id','quantity', 'customizations', 'id', 'order', 'menu_item', 'menu_item_id', 'order_id',]

    def create(self, validated_data):
        menu_item_id = validated_data.pop('menu_item_id', None)
        order_id = validated_data.pop('order_id', None)
        if menu_item_id:
            try:
                menu_item = MenuItem.objects.get(pk=menu_item_id)
                validated_data['menu_item'] = menu_item
            except MenuItem.DoesNotExist:
                raise serializers.ValidationError("MenuItem not found.")
            
        if order_id:
            try:
                order = Order.objects.get(pk=order_id)
                validated_data['order'] = order
            except Order.DoesNotExist:
                raise serializers.ValidationError("Order not found.")
        
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        menu_item_id = validated_data.pop('menu_item_id', None)
        order_id = validated_data.pop('order_id', None)
        
        if menu_item_id:
            try:
                menu_item = MenuItem.objects.get(pk=menu_item_id)
                instance.menu_item = menu_item
            except MenuItem.DoesNotExist:
                raise serializers.ValidationError("MenuItem not found.")
            
        if order_id:
            try:
                order = Order.objects.get(pk=order_id)
                instance.order = order
            except Order.DoesNotExist:
                raise serializers.ValidationError("Order not found.")

        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.customizations = validated_data.get('customizations', instance.customizations)
        
        instance.save()
        return instance
    