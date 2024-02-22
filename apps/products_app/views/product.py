from rest_framework import permissions, viewsets

from apps.common.views import ActionsForNonDeletableItemsViewMixin, CommonViewMixin
from apps.products_app.models import Product
from apps.products_app.serializers import ProductSerializer
from apps.products_app.filters import ProductFilter
from apps.products_app.serializers.product import ProductReadSerializer


class ProductViewSet(
    viewsets.ModelViewSet, CommonViewMixin, ActionsForNonDeletableItemsViewMixin
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    search_fields = ["name"]
    filterset_class = ProductFilter

    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ["GET"]:
            return ProductReadSerializer
        return ProductSerializer
