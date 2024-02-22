from rest_framework import serializers

from apps.common.serializers import BaseModelSerializer
from apps.products_app.models import Production, Product
from django.utils.translation import gettext_lazy as _

from apps.products_app.serializers import (
    GroupingPackagingReadSerializer,
    ProductReadSerializer,
)
from apps.products_app.serializers.format import FormatSerializer
from apps.products_app.serializers.plan import PlanReadSerializer


class ProductionSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Production
        fields = BaseModelSerializer.Meta.fields + [
            "id",
            "plan",
            "name",
            "product",
            "distribution_format",
            "wholesale_price",
            "quantity",
            "cost",
            "description",
            "active",
            "production_date",
        ]

    def validate(self, data):
        plan = data["plan"]

        allowed_product_kinds = plan.product_kind.get_all_children_recursively()

        allowed_products = Product.objects.filter(
            classification__in=allowed_product_kinds, historical_vault__isnull=True
        ).values_list("id", flat=True)
        product = data["product"]
        if product.id not in allowed_products:
            raise serializers.ValidationError(
                _("This product is not allowed for this plan")
            )
        return data


class ProductionReadSerializer(ProductionSerializer):
    product = ProductReadSerializer(read_only=True)
    distribution_format = GroupingPackagingReadSerializer(read_only=True)
    plan = PlanReadSerializer(read_only=True)
    format = FormatSerializer(read_only=True)

    class Meta(ProductionSerializer.Meta):
        model = Production
        fields = ProductionSerializer.Meta.fields + [
            "plan",
            "name",
            "product",
            "distribution_format",
            "format",
        ]
