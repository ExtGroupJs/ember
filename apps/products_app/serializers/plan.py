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

    total = serializers.FloatField(read_only=True)

    class Meta(BaseModelSerializer.Meta):
        model = Plan
        fields = BaseModelSerializer.Meta.fields + [
            "id",
            "name",
            "ueb",
            "destiny",
            "product_kind",
            "year",
            "jan_quantity",
            "feb_quantity",
            "mar_quantity",
            "apr_quantity",
            "may_quantity",
            "jun_quantity",
            "jul_quantity",
            "aug_quantity",
            "sep_quantity",
            "oct_quantity",
            "nov_quantity",
            "dec_quantity",
            "measurement_unit",
            "total",
        ]

    def validate_year(self, value):
        if value < self.date.year:
            raise serializers.ValidationError(
                f"El año no puede ser menor a {self.date.year}"
            )
        return value


class PlanReadSerializer(PlanSerializer):
    measurement_unit = MeasurementUnitSerializer()
    ueb = EntitySerializer()
    destiny = DestinationSerializer()
    product_kind = ClassificationSerializer()

    # def get_acumulated_quantity(self, obj) -> int:  # TODO implementar como annotation VERIFICAR SI ES NECESARIO
    #     pass
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


class MonthPlanSerializer(serializers.Serializer):
    month = serializers.IntegerField(
        min_value=Plan.Months.ENE, max_value=Plan.Months.DIC
    )
    quantity = serializers.FloatField(min_value=0)


# class YearPlanSerializer(serializers.Serializer):  TODO VALORAR SI ES NECESARIO
#     name = serializers.CharField()
#     measurement_unit = serializers.PrimaryKeyRelatedField(
#         queryset=MeasurementUnit.objects.all().only("id")
#     )
#     ueb = serializers.PrimaryKeyRelatedField(queryset=Entity.objects.all().only("id"))
#     destiny = serializers.PrimaryKeyRelatedField(
#         queryset=Destination.objects.all().only("id")
#     )
#     month_plans = serializers.CharField()

#     product_kind = serializers.PrimaryKeyRelatedField(
#         queryset=Classification.objects.all().only("id")
#     )
#     year = serializers.IntegerField(min_value=2000, max_value=2050)

#     def validate_month_plans(self, value):
#         try:
#             value = json.loads(value)
#         except Exception as e:
#             raise serializers.ValidationError(e) from None
#         serializer = MonthPlanSerializer(data=value, many=True)
#         serializer.is_valid(raise_exception=True)
#         if len(value) != 12:
#             raise serializers.ValidationError(
#                 "Falta o sobra información relativa a los planes mensuales"
#             ) from None
#         return value

#     def save(self):
#         name = self.validated_data["name"]
#         measurement_unit = self.validated_data["measurement_unit"]
#         ueb = self.validated_data["ueb"]
#         destiny = self.validated_data["destiny"]
#         product_kind = self.validated_data["product_kind"]
#         year = self.validated_data["year"]
#         month_plans = self.validated_data["month_plans"]
#         plans_to_create = []
#         for month_plan in month_plans:
#             month = month_plan["month"]
#             plans_to_create.append(
#                 Plan(
#                     name=f"{name} <{ueb}> ({product_kind}) {Plan.Months(month).label} - {year}",
#                     measurement_unit=measurement_unit,
#                     ueb=ueb,
#                     destiny=destiny,
#                     product_kind=product_kind,
#                     year=year,
#                     month=month,
#                     quantity=month_plan["quantity"],
#                 )
#             )
#         try:
#             Plan.objects.bulk_create(plans_to_create)
#         except Exception as e:
#             raise serializers.ValidationError(e)
#         return len(plans_to_create)
