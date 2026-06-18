from django.db import models


class RoomType(models.TextChoices):
    SINGLE = 'single', 'Chambre Simple'
    DOUBLE = 'double', 'Chambre Double'
    SUITE = 'suite', 'Suite'
    FAMILY = 'family', 'Chambre Familiale'
    DELUXE = 'deluxe', 'Chambre Deluxe'


class RoomStatus(models.TextChoices):
    AVAILABLE = 'available', 'Disponible'
    OCCUPIED = 'occupied', 'Occupée'
    MAINTENANCE = 'maintenance', 'En maintenance'
    CLEANING = 'cleaning', 'En nettoyage'


class Room(models.Model):
    number = models.CharField(max_length=10, unique=True, verbose_name='Numéro')
    room_type = models.CharField(max_length=20, choices=RoomType.choices, verbose_name='Type')
    floor = models.PositiveIntegerField(verbose_name='Étage')
    capacity = models.PositiveIntegerField(default=2, verbose_name='Capacité')
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Prix/nuit')
    status = models.CharField(max_length=20, choices=RoomStatus.choices, default=RoomStatus.AVAILABLE)
    description = models.TextField(blank=True, verbose_name='Description')
    has_wifi = models.BooleanField(default=True, verbose_name='WiFi')
    has_ac = models.BooleanField(default=True, verbose_name='Climatisation')
    has_tv = models.BooleanField(default=True, verbose_name='TV')
    has_minibar = models.BooleanField(default=False, verbose_name='Minibar')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['number']
        verbose_name = 'Chambre'
        verbose_name_plural = 'Chambres'

    def __str__(self):
        return f"Chambre {self.number} ({self.get_room_type_display()})"
