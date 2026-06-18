from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
    openapi.Info(
        title="🏨 Hotel Management API",
        default_version='v1',
        description="""
## API de Gestion Hôtelière

Backend complet pour la gestion d'un hôtel incluant :
- 🛏️ **Chambres** : Gestion du parc de chambres et disponibilités
- 👤 **Clients** : Profils et historique des clients
- 📅 **Réservations** : Cycle complet (création → check-in → check-out)
- 🧾 **Facturation** : Factures, lignes de facture et paiements

### Authentification
Utiliser le endpoint `/api/auth/token/` pour obtenir un token JWT.
Inclure le header : `Authorization: Bearer <token>`
        """,
        terms_of_service="https://www.hotel.com/terms/",
        contact=openapi.Contact(email="admin@hotel.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth JWT
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # API Apps
    path('api/', include('rooms.urls')),
    path('api/', include('guests.urls')),
    path('api/', include('reservations.urls')),
    path('api/', include('billing.urls')),

    # Swagger Documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]
