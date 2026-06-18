from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Reservation, ReservationStatus
from .serializers import ReservationSerializer, CheckInSerializer, CheckOutSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des réservations.
    Inclut les opérations de check-in et check-out.
    """
    queryset = Reservation.objects.select_related('room', 'guest', 'created_by').all()
    serializer_class = ReservationSerializer
    filterset_fields = ['status', 'room', 'guest', 'check_in_date', 'check_out_date']
    search_fields = ['guest__first_name', 'guest__last_name', 'guest__email', 'room__number']
    ordering_fields = ['check_in_date', 'check_out_date', 'created_at', 'total_price']

    @swagger_auto_schema(
        operation_description="Effectuer le check-in d'un client",
        request_body=CheckInSerializer,
        responses={200: ReservationSerializer}
    )
    @action(detail=True, methods=['post'], url_path='check-in')
    def check_in(self, request, pk=None):
        """Enregistrer l'arrivée du client (check-in)."""
        reservation = self.get_object()
        if reservation.status != ReservationStatus.CONFIRMED:
            return Response(
                {'error': f"Impossible d'effectuer le check-in. Statut actuel: {reservation.get_status_display()}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        reservation.do_check_in()
        return Response(ReservationSerializer(reservation).data)

    @swagger_auto_schema(
        operation_description="Effectuer le check-out d'un client",
        request_body=CheckOutSerializer,
        responses={200: ReservationSerializer}
    )
    @action(detail=True, methods=['post'], url_path='check-out')
    def check_out(self, request, pk=None):
        """Enregistrer le départ du client (check-out)."""
        reservation = self.get_object()
        if reservation.status != ReservationStatus.CHECKED_IN:
            return Response(
                {'error': f"Impossible d'effectuer le check-out. Statut actuel: {reservation.get_status_display()}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        reservation.do_check_out()
        return Response(ReservationSerializer(reservation).data)

    @swagger_auto_schema(
        operation_description="Annuler une réservation",
        responses={200: ReservationSerializer}
    )
    @action(detail=True, methods=['post'], url_path='cancel')
    def cancel(self, request, pk=None):
        """Annuler une réservation."""
        reservation = self.get_object()
        if reservation.status in [ReservationStatus.CHECKED_OUT, ReservationStatus.CANCELLED]:
            return Response({'error': 'Réservation déjà terminée ou annulée.'}, status=status.HTTP_400_BAD_REQUEST)
        reservation.status = ReservationStatus.CANCELLED
        reservation.save()
        if reservation.room.status == 'occupied':
            reservation.room.status = 'available'
            reservation.room.save()
        return Response(ReservationSerializer(reservation).data)

    @swagger_auto_schema(
        operation_description="Confirmer une réservation en attente",
        responses={200: ReservationSerializer}
    )
    @action(detail=True, methods=['post'], url_path='confirm')
    def confirm(self, request, pk=None):
        """Confirmer une réservation en attente."""
        reservation = self.get_object()
        if reservation.status != ReservationStatus.PENDING:
            return Response({'error': 'Seules les réservations en attente peuvent être confirmées.'}, status=status.HTTP_400_BAD_REQUEST)
        reservation.status = ReservationStatus.CONFIRMED
        reservation.save()
        return Response(ReservationSerializer(reservation).data)
