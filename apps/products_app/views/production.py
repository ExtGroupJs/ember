from rest_framework import permissions, viewsets

from apps.common.views import ActionsForNonDeletableItemsViewMixin, CommonViewMixin
from apps.products_app.models import Production
from apps.products_app.serializers import (
    ProductionReadSerializer,
    ProductionSerializer,
)
from apps.products_app.filters import ProductionFilter


class ProductionViewSet(
    viewsets.ModelViewSet, CommonViewMixin, ActionsForNonDeletableItemsViewMixin
):
    queryset = Production.objects.all()
    serializer_class = ProductionReadSerializer
    filterset_class = ProductionFilter
    ordering_fields = [field.name for field in queryset.model._meta.fields] + [
        "entity__name"
    ]

    search_fields = [
        "name",
        "product__name",
        "product__classification__name",
        "distribution_format__name",
        "entity__name",
    ]

    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ["GET"]:
            return ProductionReadSerializer
        return ProductionSerializer
