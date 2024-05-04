from django.urls import path
from .views import LoginView, CustomerListCreateAPIView, CustomerRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('customers/', CustomerListCreateAPIView.as_view(), name='customer_list_create'),
    path('customers/<int:pk>/', CustomerRetrieveUpdateDestroyAPIView.as_view(), name='user_retrieve_update_destroy'),
] 
