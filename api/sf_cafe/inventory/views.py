from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Inventory
from .serializers import InventorySerializer
from rest_framework.permissions import IsAuthenticated
from sf_cafe.menu_items.models import MenuItem  


class InventoryUpsertAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, menu_item_id):
        try:
            menu_item = MenuItem.objects.get(pk=menu_item_id)
        except MenuItem.DoesNotExist:
            return Response({"message": "MenuItem not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            inventory = Inventory.objects.get(menu_item=menu_item)
            serializer = InventorySerializer(instance=inventory, data=request.data)
        except Inventory.DoesNotExist:
            serializer = InventorySerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.validated_data['menu_item'] = menu_item
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
