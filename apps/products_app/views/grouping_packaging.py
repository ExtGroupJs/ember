from rest_framework import permissions, viewsets

from apps.common.views import ActionsForNonDeletableItemsViewMixin, CommonViewMixin
from apps.products_app.filters import GroupingPackagingFilter
from apps.products_app.models import GroupingPackaging
from apps.products_app.serializers import (
    GroupingPackagingReadSerializer,
    GroupingPackagingSerializer,
)


class GroupingPackagingViewSet(
    viewsets.ModelViewSet,
    CommonViewMixin,
    ActionsForNonDeletableItemsViewMixin,
):
    queryset = GroupingPackaging.objects.filter(historical_vault__isnull=True).select_related(
        "individual_packaging__measurement_unit"
    )
    serializer_class = GroupingPackagingSerializer
    filterset_class = GroupingPackagingFilter
    search_fields = ["name", "description"]

    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ["GET"]:
            return GroupingPackagingReadSerializer
        return GroupingPackagingSerializer
