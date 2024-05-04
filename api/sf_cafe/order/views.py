from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Order, OrderDetail
from .serializers import OrderSerializer, OrderDetailSerializer


class OrderListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        if not request.user.is_staff:
            serializer.save(customer=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
        customer_id = request.data['customer']
        serializer.save(customer_id=customer_id)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.filter(status='open').order_by('-order_date')

        return Order.objects.filter(customer=self.request.user).order_by('-order_date')


class OrderRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.status == 'finished':
            instance.payied_at = timezone.now() 
            instance.save()


class OrderDetailListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = OrderDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return OrderDetail.objects.all().order_by('-id')  

        return OrderDetail.objects.filter(order__client=user).order_by('-id')

    def perform_create(self, serializer):
        serializer.save()


class OrderDetailRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    

class OrderDetailByOrderIdListAPIView(generics.ListAPIView):
    serializer_class = OrderDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        order_id = self.kwargs.get('pk')
        return OrderDetail.objects.filter(order=order_id)

