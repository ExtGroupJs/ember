from rest_framework import permissions, viewsets

from apps.common.views import ActionsForNonDeletableItemsViewMixin, CommonViewMixin
from apps.products_app.models import IndividualPackaging
from apps.products_app.serializers import IndividualPackagingSerializer
from apps.products_app.serializers.grouping_packaging import (
    IndividualPackagingReadSerializer,
)


class IndividualPackagingViewSet(
    viewsets.ModelViewSet,
    CommonViewMixin,
    ActionsForNonDeletableItemsViewMixin,
):
    queryset = IndividualPackaging.objects.all().select_related("measurement_unit")
    serializer_class = IndividualPackagingSerializer
    search_fields = ["name", "description"]

    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ["GET"]:
            return IndividualPackagingReadSerializer
        return IndividualPackagingSerializer

