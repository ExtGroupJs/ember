from rest_framework import serializers

from apps.common.serializers import BaseModelSerializer
from apps.products_app.models import IndividualPackaging
from apps.products_app.serializers.measurement_unit import MeasurementUnitSerializer


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
    name_representation = serializers.SerializerMethodField()

    class Meta(IndividualPackagingSerializer.Meta):
        model = IndividualPackaging
        fields = IndividualPackagingSerializer.Meta.fields + ["name_representation"]

    def get_name_representation(self, obj) -> str:
        return str(obj)
