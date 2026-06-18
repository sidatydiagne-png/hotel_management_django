from rest_framework import serializers
from .models import Invoice, InvoiceItem, Payment
from django.utils import timezone


class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = '__all__'
        read_only_fields = ['total']


class PaymentSerializer(serializers.ModelSerializer):
    method_display = serializers.CharField(source='get_method_display', read_only=True)

    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ['paid_at']


class InvoiceSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True, read_only=True)
    payments = PaymentSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Invoice
        fields = '__all__'
        read_only_fields = ['invoice_number', 'created_at', 'updated_at', 'tax_amount', 'total_amount', 'subtotal']

    def create(self, validated_data):
        validated_data['invoice_number'] = Invoice.generate_invoice_number()
        invoice = super().create(validated_data)
        invoice.calculate_totals()
        return invoice
