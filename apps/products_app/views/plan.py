from rest_framework.response import Response
from rest_framework import permissions, viewsets, status

from apps.common.views import ActionsForNonDeletableItemsViewMixin, CommonViewMixin
from apps.products_app.models import Plan
from apps.products_app.models.product import Product
from apps.products_app.serializers import PlanReadSerializer
from rest_framework.decorators import action

from apps.products_app.serializers import PlanSerializer
from apps.products_app.serializers.product import ProductSerializer


# from apps.products_app.filters import PlanFilter


class PlanViewSet(
    viewsets.ModelViewSet, CommonViewMixin, ActionsForNonDeletableItemsViewMixin
):
    queryset = Plan.objects.all()
    serializer_class = PlanReadSerializer
    search_fields = ["name"]
    # filterset_class = PlanFilter

    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ["GET"]:
            return PlanReadSerializer
        return PlanSerializer

    # TODO add tests for this viewset
    @action(
        detail=True,
        methods=["GET"],
        url_name="acumulated-quantity",
        url_path="acumulated-quantity",
    )
    def acumulated_quantity(self, request, pk=None) -> int:
        obj = self.get_object()
        acumulated = Plan.objects.filter(
            product=obj.product, year=obj.year, month__lte=obj.month
        )
        acumulated_quantity_hectoliters = 0
        acumulated_quantity_thousands_of_boxes = 0
        for plan in acumulated:
            if plan.measurement_unit == "H":
                acumulated_quantity_hectoliters += plan.quantity
            elif plan.measurement_unit == "M":
                acumulated_quantity_thousands_of_boxes += plan.quantity
        response_data = {
            "hetolitros": acumulated_quantity_hectoliters,
            "miles_de_cajas": acumulated_quantity_thousands_of_boxes,
        }

        return Response(response_data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["GET"],
        url_name="allowed-products",
        url_path="allowed-products",
    )
    def allowed_products(self, request, pk=None) -> Response:
        obj = self.get_object()
        allowed_product_kinds = obj.product_kind.get_all_children_recursively()
        allowed_products = Product.objects.select_related("classification").filter(
            classification__in=allowed_product_kinds, historical_vault__isnull=True
        )
        if not allowed_products:
            return Response(
                "No hay productos disponibles para este plan",
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = ProductSerializer(allowed_products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
