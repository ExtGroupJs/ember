from rest_framework import serializers

from apps.common.serializers import BaseModelSerializer
from apps.products_app.models import (
    GroupingPackaging,
    IndividualPackaging,
    MeasurementUnit,
)


class MeasurementUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeasurementUnit
        fields = [
            "id",
            "name",
            "symbol",
            "description",
            "mililiters",
            "used_for_planning",
        ]


class IndividualPackagingSerializer(BaseModelSerializer):

    class Meta(BaseModelSerializer.Meta):
        model = IndividualPackaging
        fields = BaseModelSerializer.Meta.fields + [
            "id",
            "name",
            "description",
            "capacity",
            "measurement_unit",
            "is_grouping_packaging",
        ]

class IndividualPackagingReadSerializer(IndividualPackagingSerializer):
    measurement_unit = MeasurementUnitSerializer()
    name = serializers.SerializerMethodField()
    
    class Meta(IndividualPackagingSerializer.Meta):
        model = IndividualPackaging
    def get_name(self, obj):
        return str(obj)

class GroupingPackagingSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = GroupingPackaging
        fields = BaseModelSerializer.Meta.fields + [
            "id",
            "name",
            "description",
            "capacity",
            "individual_packaging",
        ]

    def get_representation(self, obj):
        return str(obj)

    def get_total_mililiters(self, obj):
        individual_packaging = obj.individual_packaging
        brute_qty = (
            individual_packaging.capacity
            * obj.capacity
            * individual_packaging.measurement_unit.mililiters
        )
        return brute_qty


class GroupingPackagingReadSerializer(GroupingPackagingSerializer):
    individual_packaging = IndividualPackagingReadSerializer()
    representation = serializers.SerializerMethodField()
    total_mililiters = serializers.SerializerMethodField()

    class Meta(GroupingPackagingSerializer.Meta):
        model = GroupingPackaging
        fields = GroupingPackagingSerializer.Meta.fields + [
            "representation",
            "total_mililiters",
            "individual_packaging",
        ]
