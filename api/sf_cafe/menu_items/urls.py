from django.urls import path
from .views import MenuItemListCreateAPIView, MenuItemRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('menu-items/', MenuItemListCreateAPIView.as_view(), name='get_menu_items'),
    path('menu-items/<int:pk>/', MenuItemRetrieveUpdateDestroyAPIView.as_view(), name='menu_item_retrieve_update_destroy'),
] 
