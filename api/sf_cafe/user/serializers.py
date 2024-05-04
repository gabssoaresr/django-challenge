from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'name',
            'email',
            'phone',
            'is_active',
            'is_staff',
            'is_superuser',
        )

class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'name',
            'email',
            'phone',
        )