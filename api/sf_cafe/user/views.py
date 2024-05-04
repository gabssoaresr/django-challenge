from django.http import JsonResponse
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserSerializer, CustomerSerializer
from .models import User


class LoginView(APIView):
    permission_classes = [AllowAny]

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not email:
            return JsonResponse({'error': 'Email is required'}, status=400)
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User with this email does not exist'}, status=404)

        if not user.is_staff:
            token, created = Token.objects.get_or_create(user=user)
            serializer = UserSerializer(user)
            response_data = {
                'user': serializer.data,
                'token': token.key
            }
            return JsonResponse(response_data)
        

        if not password:
            return JsonResponse({'error': 'Password is required for admin/employee login'}, status=400)
        authenticated_user = authenticate(request, email=email, password=password)
        if not authenticated_user:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
        token, created = Token.objects.get_or_create(user=user)
        serializer = UserSerializer(user)
        response_data = {
            'user': serializer.data,
            'token': token.key
        }
        return JsonResponse(response_data)

class CustomerListCreateAPIView(generics.ListCreateAPIView):
    queryset = User.objects.filter(is_staff=False)
    serializer_class = CustomerSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(is_staff=False, is_superuser=False)
        user = serializer.save(is_staff=False, is_superuser=False)
        raw_password = User.objects.make_random_password()
        user.set_password(raw_password)
        user.save()

    def get_queryset(self):
        queryset = User.objects.filter(is_staff=False)
        email = self.request.query_params.get('email')
        if email:
            queryset = queryset.filter(email__icontains=email)
        return queryset
    
class CustomerRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.filter(is_staff=False)
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save(is_staff=False, is_superuser=False)
