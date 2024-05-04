import json
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from .models import MenuItem
from .serializers import MenuItemSerializer, InventorySerializer, Inventory


class MenuItemListCreateAPIView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        item_name = self.request.query_params.get('name')
        queryset = super().get_queryset()
        
        if item_name:
            return queryset.filter(name__icontains=item_name, inventory__available_quantity__gt=0)
     
        return queryset.filter()

        
class MenuItemRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    @transaction.atomic
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        inventory_instance = instance.inventory

        if not inventory_instance:
            return Response({'inventory': ['Inventory does not exist for this MenuItem.']}, status=status.HTTP_400_BAD_REQUEST)

        inventory_serializer = InventorySerializer(inventory_instance, data=request.data, partial=True)
        inventory_serializer.is_valid(raise_exception=True)
        inventory_serializer.save()

        return Response(inventory_serializer.data)