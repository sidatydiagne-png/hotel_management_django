from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Invoice, InvoiceItem, Payment, InvoiceStatus
from .serializers import InvoiceSerializer, InvoiceItemSerializer, PaymentSerializer


class InvoiceViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des factures.
    """
    queryset = Invoice.objects.select_related('reservation').prefetch_related('items', 'payments').all()
    serializer_class = InvoiceSerializer
    filterset_fields = ['status', 'reservation']
    ordering_fields = ['created_at', 'total_amount']

    @swagger_auto_schema(
        operation_description="Émettre une facture (statut: brouillon -> émise)",
        responses={200: InvoiceSerializer}
    )
    @action(detail=True, methods=['post'], url_path='issue')
    def issue(self, request, pk=None):
        """Émettre officiellement une facture."""
        invoice = self.get_object()
        if invoice.status != InvoiceStatus.DRAFT:
            return Response({'error': 'Seuls les brouillons peuvent être émis.'}, status=status.HTTP_400_BAD_REQUEST)
        invoice.status = InvoiceStatus.ISSUED
        invoice.issued_at = timezone.now()
        invoice.calculate_totals()
        return Response(InvoiceSerializer(invoice).data)

    @swagger_auto_schema(
        operation_description="Marquer une facture comme payée",
        request_body=PaymentSerializer,
        responses={200: InvoiceSerializer}
    )
    @action(detail=True, methods=['post'], url_path='pay')
    def pay(self, request, pk=None):
        """Enregistrer un paiement pour cette facture."""
        invoice = self.get_object()
        serializer = PaymentSerializer(data={**request.data, 'invoice': invoice.pk})
        if serializer.is_valid():
            serializer.save()
            invoice.status = InvoiceStatus.PAID
            invoice.paid_at = timezone.now()
            invoice.save()
            return Response(InvoiceSerializer(invoice).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='add-item')
    def add_item(self, request, pk=None):
        """Ajouter une ligne à la facture."""
        invoice = self.get_object()
        serializer = InvoiceItemSerializer(data={**request.data, 'invoice': invoice.pk})
        if serializer.is_valid():
            serializer.save()
            invoice.calculate_totals()
            return Response(InvoiceSerializer(invoice).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet pour consulter les paiements (lecture seule).
    """
    queryset = Payment.objects.select_related('invoice').all()
    serializer_class = PaymentSerializer
    filterset_fields = ['method', 'invoice']
    ordering_fields = ['paid_at', 'amount']
