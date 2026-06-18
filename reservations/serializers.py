from rest_framework import serializers
from .models import Reservation
from rooms.serializers import RoomListSerializer
from guests.serializers import GuestListSerializer


class ReservationSerializer(serializers.ModelSerializer):
    nights = serializers.ReadOnlyField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    room_detail = RoomListSerializer(source='room', read_only=True)
    guest_detail = GuestListSerializer(source='guest', read_only=True)

    class Meta:
        model = Reservation
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'total_price', 'price_per_night', 'actual_check_in', 'actual_check_out', 'created_by']

    def validate(self, data):
        check_in = data.get('check_in_date')
        check_out = data.get('check_out_date')
        room = data.get('room')
        instance = self.instance

        if check_in and check_out and check_out <= check_in:
            raise serializers.ValidationError("La date de départ doit être après la date d'arrivée.")

        if room and check_in and check_out:
            conflicts = Reservation.objects.filter(
                room=room,
                status__in=['pending', 'confirmed', 'checked_in'],
                check_in_date__lt=check_out,
                check_out_date__gt=check_in,
            )
            if instance:
                conflicts = conflicts.exclude(pk=instance.pk)
            if conflicts.exists():
                raise serializers.ValidationError("Cette chambre est déjà réservée pour ces dates.")
        return data

    def create(self, validated_data):
        validated_data['price_per_night'] = validated_data['room'].price_per_night
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class CheckInSerializer(serializers.Serializer):
    confirm = serializers.BooleanField(default=True)


class CheckOutSerializer(serializers.Serializer):
    confirm = serializers.BooleanField(default=True)
