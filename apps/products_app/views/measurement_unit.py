from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets

from apps.products_app.models import MeasurementUnit
from apps.products_app.serializers import MeasurementUnitSerializer


class MeasurementUnitViewSet(viewsets.ModelViewSet):
    queryset = MeasurementUnit.objects.all()
    serializer_class = MeasurementUnitSerializer
    search_fields = ["name", "symbol"]
    filter_backends = [
        DjangoFilterBackend,
    ]
    filterset_fields = [
        "used_for_planning",
    ]

    permission_classes = [permissions.IsAuthenticated]

