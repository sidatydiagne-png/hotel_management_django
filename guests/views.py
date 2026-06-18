from rest_framework import viewsets
from drf_yasg.utils import swagger_auto_schema
from .models import Guest
from .serializers import GuestSerializer, GuestListSerializer


class GuestViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des clients de l'hôtel.
    """
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    filterset_fields = ['nationality', 'country']
    search_fields = ['first_name', 'last_name', 'email', 'id_number', 'phone']
    ordering_fields = ['last_name', 'created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return GuestListSerializer
        return GuestSerializer
