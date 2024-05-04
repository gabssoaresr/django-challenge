from django.urls import path
from .views import InventoryUpsertAPIView

urlpatterns = [
    path('menu-items/<int:menu_item_id>/inventory/', InventoryUpsertAPIView.as_view(), name='inventory_upsert'),
]
