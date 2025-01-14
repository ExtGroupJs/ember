import datetime
from rest_framework import serializers

from apps.common.serializers import BaseModelSerializer
from apps.products_app.models import Plan
from apps.products_app.serializers import (
    ClassificationSerializer,
    DestinationSerializer,
    EntitySerializer,
    MeasurementUnitSerializer,
)


class PlanSerializer(BaseModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.date = datetime.date.today()
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
    def validate_year(self, value):
        if value < self.date.year:
            raise serializers.ValidationError(f"El año no puede ser menor a {self.date.year}")
        return value    
    def validate(self, attrs):
        year = attrs["year"]
        if year == self.date.year:
            month = attrs["month"]
            if month < self.date.month:
                raise serializers.ValidationError(f"El mes no puede ser menor al actual")
        return attrs

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

    def get_month(self, obj) -> str:
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
