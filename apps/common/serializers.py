from rest_framework import serializers

from apps.common.models import BaseModel, HistoricalVault


class ArchiveItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalVault
        fields = ["id", "deletion_cause"]

    def validate_deletion_cause(self, value):
        if value == "":
            return "NO DELETION CAUSE WAS PROVIDED"
        return value


class BaseModelSerializer(serializers.ModelSerializer):
    deletion_timestamp = serializers.DateTimeField(
        source="historical_vault.deletion_timestamp", default=None, read_only=True
    )
    deletion_cause = serializers.CharField(
        source="historical_vault.deletion_cause", default=None, read_only=True
    )
    deleted_by = serializers.CharField(
        source="historical_vault.author.username", default=None, read_only=True
    )
    historical_vault = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = BaseModel
        fields = [
            "id",
            "created_timestamp",
            "updated_timestamp",
            "historical_vault",
            "deletion_timestamp",
            "deletion_cause",
            "deleted_by",
        ]
        read_only_fields = ("historical_vault",)
