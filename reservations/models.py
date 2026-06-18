from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class ReservationStatus(models.TextChoices):
    PENDING = 'pending', 'En attente'
    CONFIRMED = 'confirmed', 'Confirmée'
    CHECKED_IN = 'checked_in', 'Enregistrée'
    CHECKED_OUT = 'checked_out', 'Terminée'
    CANCELLED = 'cancelled', 'Annulée'
    NO_SHOW = 'no_show', 'Non présenté'


class Reservation(models.Model):
    room = models.ForeignKey('rooms.Room', on_delete=models.PROTECT, related_name='reservations', verbose_name='Chambre')
    guest = models.ForeignKey('guests.Guest', on_delete=models.PROTECT, related_name='reservations', verbose_name='Client')
    check_in_date = models.DateField(verbose_name='Date arrivée')
    check_out_date = models.DateField(verbose_name='Date départ')
    actual_check_in = models.DateTimeField(null=True, blank=True, verbose_name='Arrivée réelle')
    actual_check_out = models.DateTimeField(null=True, blank=True, verbose_name='Départ réel')
    status = models.CharField(max_length=20, choices=ReservationStatus.choices, default=ReservationStatus.PENDING)
    adults = models.PositiveIntegerField(default=1, verbose_name='Adultes')
    children = models.PositiveIntegerField(default=0, verbose_name='Enfants')
    special_requests = models.TextField(blank=True, verbose_name='Demandes spéciales')
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Prix/nuit')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Prix total')
    created_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='created_reservations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Réservation'
        verbose_name_plural = 'Réservations'

    def __str__(self):
        return f"Réservation #{self.pk} - {self.guest} - Chambre {self.room.number}"

    @property
    def nights(self):
        return (self.check_out_date - self.check_in_date).days

    def clean(self):
        if self.check_in_date and self.check_out_date:
            if self.check_out_date <= self.check_in_date:
                raise ValidationError("La date de départ doit être après la date d'arrivée.")

    def save(self, *args, **kwargs):
        if self.check_in_date and self.check_out_date and self.price_per_night:
            self.total_price = self.price_per_night * self.nights
        super().save(*args, **kwargs)

    def do_check_in(self):
        self.actual_check_in = timezone.now()
        self.status = ReservationStatus.CHECKED_IN
        self.room.status = 'occupied'
        self.room.save()
        self.save()

    def do_check_out(self):
        self.actual_check_out = timezone.now()
        self.status = ReservationStatus.CHECKED_OUT
        self.room.status = 'cleaning'
        self.room.save()
        self.save()
