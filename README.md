

Backend Django REST Framework pour la gestion complète d'un hôtel.

## 🚀 Installation

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## 📚 Documentation API

| URL | Description |
|-----|-------------|
| `/swagger/` | Documentation Swagger interactive |
| `/redoc/` | Documentation ReDoc |
| `/admin/` | Interface d'administration |

## 🔐 Authentification JWT

```bash
# Obtenir un token
POST /api/auth/token/
{ "username": "admin", "password": "admin123" }

# Utiliser le token
Authorization: Bearer <access_token>

# Rafraîchir le token
POST /api/auth/token/refresh/
{ "refresh": "<refresh_token>" }
```

## 📡 Endpoints API

### 🛏️ Chambres `/api/rooms/`
| Méthode | URL | Action |
|---------|-----|--------|
| GET | `/api/rooms/` | Lister toutes les chambres |
| POST | `/api/rooms/` | Créer une chambre |
| GET | `/api/rooms/{id}/` | Détail d'une chambre |
| PUT/PATCH | `/api/rooms/{id}/` | Modifier une chambre |
| DELETE | `/api/rooms/{id}/` | Supprimer une chambre |
| GET | `/api/rooms/available/` | Chambres disponibles |
| PATCH | `/api/rooms/{id}/change-status/` | Changer le statut |

### 👤 Clients `/api/guests/`
| Méthode | URL | Action |
|---------|-----|--------|
| GET | `/api/guests/` | Lister les clients |
| POST | `/api/guests/` | Créer un client |
| GET | `/api/guests/{id}/` | Détail client |
| PUT/PATCH | `/api/guests/{id}/` | Modifier un client |
| DELETE | `/api/guests/{id}/` | Supprimer un client |

### 📅 Réservations `/api/reservations/`
| Méthode | URL | Action |
|---------|-----|--------|
| GET | `/api/reservations/` | Lister les réservations |
| POST | `/api/reservations/` | Créer une réservation |
| GET | `/api/reservations/{id}/` | Détail réservation |
| PUT/PATCH | `/api/reservations/{id}/` | Modifier |
| POST | `/api/reservations/{id}/confirm/` | ✅ Confirmer |
| POST | `/api/reservations/{id}/check-in/` | 🏨 Check-in |
| POST | `/api/reservations/{id}/check-out/` | 🚪 Check-out |
| POST | `/api/reservations/{id}/cancel/` | ❌ Annuler |

### 🧾 Facturation `/api/invoices/`
| Méthode | URL | Action |
|---------|-----|--------|
| GET | `/api/invoices/` | Lister les factures |
| POST | `/api/invoices/` | Créer une facture |
| GET | `/api/invoices/{id}/` | Détail facture |
| POST | `/api/invoices/{id}/issue/` | 📄 Émettre |
| POST | `/api/invoices/{id}/pay/` | 💳 Payer |
| POST | `/api/invoices/{id}/add-item/` | ➕ Ajouter ligne |

## 🔄 Cycle de vie d'une réservation

```
PENDING → CONFIRMED → CHECKED_IN → CHECKED_OUT
                    ↘ CANCELLED
                              ↘ NO_SHOW
```

## 🏗️ Architecture

```
hotel_management/
├── rooms/          # Gestion des chambres
├── guests/         # Gestion des clients
├── reservations/   # Réservations + check-in/out
├── billing/        # Factures et paiements
└── hotel_management/  # Config principale
```
