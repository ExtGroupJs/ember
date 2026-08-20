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
    default_error_messages = {
        "no_plan_provided": _("No plan provided"),
        "no_product_provided": _("No product provided"),
    }

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
            "extra_info",
            "active",
            "production_date",
        ]

    def validate(self, attrs):
        product = (
            attrs["product"] if "product" in attrs else self.fail("no_product_provided")
        )
        plan = attrs["plan"] if "plan" in attrs else self.fail("no_plan_provided")
        allowed_product_kinds = plan.product_kind.get_all_children_recursively()

        allowed_product = Product.objects.filter(
            classification__in=allowed_product_kinds,
            historical_vault__isnull=True,
            id=product.id,
        ).exists()
        if not allowed_product:
            raise serializers.ValidationError(
                _("This product is not allowed for this plan")
            )
        return attrs


class ProductionReadSerializer(ProductionSerializer):
    name = serializers.CharField(source="__str__", read_only=True)
    product = ProductReadSerializer(read_only=True)
    distribution_format = GroupingPackagingReadSerializer(read_only=True)
    plan = PlanReadSerializer(read_only=True)
    format = FormatSerializer(read_only=True)

    class Meta(ProductionSerializer.Meta):
        fields = ProductionSerializer.Meta.fields + [
            "format",
        ]
