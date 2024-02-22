from rest_framework import permissions, viewsets
from django_filters.rest_framework import DjangoFilterBackend


from apps.common.views import ActionsForNonDeletableItemsViewMixin, CommonViewMixin
from apps.products_app.models import (
    GroupingPackaging,
    IndividualPackaging,
    MeasurementUnit,
)
from apps.products_app.serializers import (
    GroupingPackagingSerializer,
    IndividualPackagingSerializer,
    MeasurementUnitSerializer,
)
from apps.products_app.filters import GroupingPackagingFilter
from apps.products_app.serializers.packaging import (
    GroupingPackagingReadSerializer,
    IndividualPackagingReadSerializer,
)


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


class GroupingPackagingViewSet(
    viewsets.ModelViewSet,
    CommonViewMixin,
    ActionsForNonDeletableItemsViewMixin,
):
    queryset = GroupingPackaging.objects.all().select_related(
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
