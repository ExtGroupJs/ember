from apps.common.serializers import BaseModelSerializer
from apps.products_app.models import Plan
from rest_framework import serializers

from apps.products_app.serializers import (
    ClassificationSerializer,
    DestinationSerializer,
    EntitySerializer,
    MeasurementUnitSerializer,
)


class PlanSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Plan
        fields = BaseModelSerializer.Meta.fields + [
            "id",
            "name",
            "ueb",
            "destiny",
            "product_kind",
            "year",
            "month",
            "quantity",
            "measurement_unit",
        ]


class PlanReadSerializer(PlanSerializer):
    acumulated_quantity = serializers.SerializerMethodField()
    measurement_unit = MeasurementUnitSerializer()
    ueb = EntitySerializer()
    destiny = DestinationSerializer()
    product_kind = ClassificationSerializer()
    month = serializers.SerializerMethodField()

    class Meta(BaseModelSerializer.Meta):
        model = Plan
        fields = PlanSerializer.Meta.fields + [
            "measurement_unit",
            "acumulated_quantity",
        ]

    def get_month(self, obj):
        return Plan.Months(obj.month).label

    def get_acumulated_quantity(self, obj) -> int:
        pass
        # acumulated = Plan.objects.filter(
        #     product=obj.product, year=obj.year, month__lte=obj.month
        # )
        # acumulated_quantity_hectoliters = 0
        # acumulated_quantity_thousands_of_boxes = 0
        # for plan in acumulated:
        #     if plan.measurement_unit == "H":
        #         acumulated_quantity_hectoliters += plan.quantity
        #     elif plan.measurement_unit == "M":
        #         acumulated_quantity_thousands_of_boxes += plan.quantity

        # return (
        #     f"hetolitros: {acumulated_quantity_hectoliters}",
        #     f"miles de cajas: {acumulated_quantity_thousands_of_boxes}",
        # )
