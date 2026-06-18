from rest_framework import serializers
from .models import Guest


class GuestSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = Guest
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class GuestListSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = Guest
        fields = ['id', 'full_name', 'first_name', 'last_name', 'email', 'phone', 'nationality']
