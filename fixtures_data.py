import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel_management.settings')
django.setup()

from rooms.models import Room
from guests.models import Guest
from reservations.models import Reservation, ReservationStatus
from datetime import date, timedelta

# Sample rooms
rooms_data = [
    {'number': '101', 'room_type': 'single', 'floor': 1, 'capacity': 1, 'price_per_night': 35000},
    {'number': '102', 'room_type': 'single', 'floor': 1, 'capacity': 1, 'price_per_night': 35000},
    {'number': '201', 'room_type': 'double', 'floor': 2, 'capacity': 2, 'price_per_night': 55000},
    {'number': '202', 'room_type': 'double', 'floor': 2, 'capacity': 2, 'price_per_night': 55000},
    {'number': '301', 'room_type': 'suite', 'floor': 3, 'capacity': 4, 'price_per_night': 120000, 'has_minibar': True},
    {'number': '302', 'room_type': 'deluxe', 'floor': 3, 'capacity': 3, 'price_per_night': 85000, 'has_minibar': True},
    {'number': '401', 'room_type': 'family', 'floor': 4, 'capacity': 5, 'price_per_night': 95000},
]
for r in rooms_data:
    Room.objects.get_or_create(number=r['number'], defaults=r)

# Sample guests
guests_data = [
    {'first_name': 'Mamadou', 'last_name': 'Diallo', 'email': 'mamadou@email.com', 'phone': '+221771234567', 'nationality': 'Sénégalaise'},
    {'first_name': 'Aïssatou', 'last_name': 'Bah', 'email': 'aissatou@email.com', 'phone': '+224621234567', 'nationality': 'Guinéenne'},
    {'first_name': 'Ibrahim', 'last_name': 'Coulibaly', 'email': 'ibrahim@email.com', 'phone': '+22500000001', 'nationality': 'Ivoirienne'},
]
for g in guests_data:
    Guest.objects.get_or_create(email=g['email'], defaults=g)

print("✅ Données de démonstration créées avec succès!")
print(f"   Chambres: {Room.objects.count()}")
print(f"   Clients: {Guest.objects.count()}")
