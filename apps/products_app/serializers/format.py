from rest_framework import serializers

from apps.products_app.models import Format


class FormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Format
        fields = [
            "id",
            "name",
            "description",
        ]
