from django.urls import path
from .views import (
    OrderDetailListCreateAPIView, 
    OrderDetailRetrieveUpdateAPIView, 
    OrderListCreateAPIView, 
    OrderRetrieveUpdateAPIView,
    OrderDetailByOrderIdListAPIView,
)


urlpatterns = [
    path('order-details/', OrderDetailListCreateAPIView.as_view(), name='order_detail_list_create'),
    path('order-details/<int:pk>/', OrderDetailRetrieveUpdateAPIView.as_view(), name='order_detail_retrieve_update'),
    path('orders/', OrderListCreateAPIView.as_view(), name='order_list_create'),
    path('orders/<int:pk>/', OrderRetrieveUpdateAPIView.as_view(), name='order_retrieve_update'),
    path('orders/<int:pk>/order-details/', OrderDetailByOrderIdListAPIView.as_view(), name='order_by_order_id_list'),
] 
