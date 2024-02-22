from rest_framework import serializers

from apps.common.serializers import BaseModelSerializer
from apps.products_app.models import Product
from apps.products_app.serializers import ClassificationSerializer
from apps.products_app.serializers.format import FormatSerializer


class ProductSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Product
        fields = BaseModelSerializer.Meta.fields + [
            "id",
            "name",
            "classification",
            "description",
            "format",
        ]
        read_only_fields = ("format",)


class ProductReadSerializer(ProductSerializer):
    classification = ClassificationSerializer()
    format = FormatSerializer(read_only=True)

    class Meta(ProductSerializer.Meta):
        model = Product
        fields = ProductSerializer.Meta.fields + [
            "classification",
            "format",
        ]
