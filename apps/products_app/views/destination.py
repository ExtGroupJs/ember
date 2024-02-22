from rest_framework import permissions, viewsets

from apps.products_app.models import Destination
from apps.products_app.serializers import DestinationSerializer


class DestinationViewSet(viewsets.ModelViewSet):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    search_fields = ["name"]

    permission_classes = [permissions.IsAuthenticated]
