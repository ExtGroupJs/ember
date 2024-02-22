from rest_framework import serializers

from apps.products_app.models import Destination


class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = [
            "id",
            "name",
            "enabled",
        ]
