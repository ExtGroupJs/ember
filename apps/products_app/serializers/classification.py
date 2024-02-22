from rest_framework import serializers

from apps.products_app.models import Classification


class ClassificationSerializer(serializers.ModelSerializer):
    full_hierarchy = serializers.CharField(source="_str_full_hierarchy", read_only=True)

    class Meta:
        model = Classification
        fields = [
            "id",
            "name",
            "description",
            "parent",
            "full_hierarchy",
        ]
        extra_kwargs = {
            "parent": {"required": True},
        }
