from rest_framework import serializers

from apps.common.serializers import BaseModelSerializer
from apps.products_app.models import GroupingPackaging
from apps.products_app.serializers.individual_packaging import (
    IndividualPackagingReadSerializer,
)


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

    def get_representation(self, obj) -> str:
        return str(obj)

    def get_total_mililiters(self, obj) -> int:
        individual_packaging = obj.individual_packaging
        brute_qty = (
            individual_packaging.capacity
            * obj.capacity
            * individual_packaging.measurement_unit.mililiters
        )
        return brute_qty
