from rest_framework import serializers
from .models import Room


class RoomSerializer(serializers.ModelSerializer):
    room_type_display = serializers.CharField(source='get_room_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Room
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class RoomListSerializer(serializers.ModelSerializer):
    room_type_display = serializers.CharField(source='get_room_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Room
        fields = ['id', 'number', 'room_type', 'room_type_display', 'floor',
                  'capacity', 'price_per_night', 'status', 'status_display']
