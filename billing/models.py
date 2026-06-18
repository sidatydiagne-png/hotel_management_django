from django.db import models


class InvoiceStatus(models.TextChoices):
    DRAFT = 'draft', 'Brouillon'
    ISSUED = 'issued', 'Émise'
    PAID = 'paid', 'Payée'
    CANCELLED = 'cancelled', 'Annulée'


class PaymentMethod(models.TextChoices):
    CASH = 'cash', 'Espèces'
    CARD = 'card', 'Carte bancaire'
    TRANSFER = 'transfer', 'Virement'
    MOBILE = 'mobile', 'Mobile Money'
    CHECK = 'check', 'Chèque'


class Invoice(models.Model):
    reservation = models.OneToOneField(
        'reservations.Reservation', on_delete=models.PROTECT,
        related_name='invoice', verbose_name='Réservation'
    )
    invoice_number = models.CharField(max_length=20, unique=True, verbose_name='N° Facture')
    status = models.CharField(max_length=20, choices=InvoiceStatus.choices, default=InvoiceStatus.DRAFT)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=18.00, verbose_name='TVA (%)')
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Remise')
    notes = models.TextField(blank=True, verbose_name='Notes')
    issued_at = models.DateTimeField(null=True, blank=True, verbose_name='Date émission')
    paid_at = models.DateTimeField(null=True, blank=True, verbose_name='Date paiement')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Facture'
        verbose_name_plural = 'Factures'

    def __str__(self):
        return f"Facture {self.invoice_number}"

    def calculate_totals(self):
        self.subtotal = self.reservation.total_price - self.discount
        self.tax_amount = self.subtotal * (self.tax_rate / 100)
        self.total_amount = self.subtotal + self.tax_amount
        self.save()

    @classmethod
    def generate_invoice_number(cls):
        import datetime
        year = datetime.date.today().year
        count = cls.objects.filter(created_at__year=year).count() + 1
        return f"FAC-{year}-{count:04d}"


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    description = models.CharField(max_length=200, verbose_name='Description')
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Prix unitaire')
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Total')

    class Meta:
        verbose_name = 'Ligne de facture'
        verbose_name_plural = 'Lignes de facture'

    def save(self, *args, **kwargs):
        self.total = self.quantity * self.unit_price
        super().save(*args, **kwargs)


class Payment(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.PROTECT, related_name='payments', verbose_name='Facture')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Montant')
    method = models.CharField(max_length=20, choices=PaymentMethod.choices, verbose_name='Méthode')
    reference = models.CharField(max_length=100, blank=True, verbose_name='Référence')
    paid_at = models.DateTimeField(auto_now_add=True, verbose_name='Date')
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-paid_at']
        verbose_name = 'Paiement'
        verbose_name_plural = 'Paiements'

    def __str__(self):
        return f"Paiement {self.amount} FCFA - {self.invoice.invoice_number}"
