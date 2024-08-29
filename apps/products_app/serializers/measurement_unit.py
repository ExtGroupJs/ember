from rest_framework import serializers

from apps.products_app.models import MeasurementUnit


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