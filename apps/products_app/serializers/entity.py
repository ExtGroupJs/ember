from rest_framework import serializers

from apps.products_app.models import Entity


class EntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = [
            "id",
            "name",
            "email",
            "enabled",
            "phone_1",
            "phone_2",
        ]
