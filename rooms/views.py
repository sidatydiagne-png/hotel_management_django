from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Room, RoomStatus
from .serializers import RoomSerializer, RoomListSerializer


class RoomViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des chambres d'hôtel.
    Permet de créer, lister, modifier et supprimer des chambres.
    """
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filterset_fields = ['room_type', 'status', 'floor', 'has_wifi', 'has_ac']
    search_fields = ['number', 'description']
    ordering_fields = ['number', 'price_per_night', 'floor']

    def get_serializer_class(self):
        if self.action == 'list':
            return RoomListSerializer
        return RoomSerializer

    @swagger_auto_schema(
        operation_description="Lister toutes les chambres disponibles",
        responses={200: RoomListSerializer(many=True)},
        manual_parameters=[
            openapi.Parameter('date_in', openapi.IN_QUERY, description="Date d'arrivée (YYYY-MM-DD)", type=openapi.TYPE_STRING),
            openapi.Parameter('date_out', openapi.IN_QUERY, description="Date de départ (YYYY-MM-DD)", type=openapi.TYPE_STRING),
        ]
    )
    @action(detail=False, methods=['get'], url_path='available')
    def available(self, request):
        """Retourne les chambres disponibles, avec filtrage optionnel par dates."""
        date_in = request.query_params.get('date_in')
        date_out = request.query_params.get('date_out')

        rooms = Room.objects.filter(status=RoomStatus.AVAILABLE)

        if date_in and date_out:
            from reservations.models import Reservation
            occupied_room_ids = Reservation.objects.filter(
                status__in=['pending', 'confirmed', 'checked_in'],
                check_in_date__lt=date_out,
                check_out_date__gt=date_in,
            ).values_list('room_id', flat=True)
            rooms = rooms.exclude(id__in=occupied_room_ids)

        serializer = RoomListSerializer(rooms, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Changer le statut d'une chambre",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={'status': openapi.Schema(type=openapi.TYPE_STRING, enum=[s.value for s in RoomStatus])},
            required=['status']
        )
    )
    @action(detail=True, methods=['patch'], url_path='change-status')
    def change_status(self, request, pk=None):
        """Changer manuellement le statut d'une chambre."""
        room = self.get_object()
        new_status = request.data.get('status')
        if new_status not in [s.value for s in RoomStatus]:
            return Response({'error': 'Statut invalide'}, status=status.HTTP_400_BAD_REQUEST)
        room.status = new_status
        room.save()
        return Response(RoomSerializer(room).data)
