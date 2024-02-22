from rest_framework import permissions, viewsets

from apps.products_app.models import Entity
from apps.products_app.serializers import EntitySerializer


class EntityViewSet(viewsets.ModelViewSet):
    queryset = Entity.objects.all()
    serializer_class = EntitySerializer
    search_fields = ["name", "email", "phone"]

    permission_classes = [permissions.IsAuthenticated]
