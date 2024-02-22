from apps.common.serializers import BaseModelSerializer
from apps.users_app.models import SystemEmail


class SystemEmailSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = SystemEmail
        fields = BaseModelSerializer.Meta.fields + [
            "id",
            "user",
            "topic",
            "text",
            "sent_date",
            "attachment",
        ]
        read_only_fields = [
            "id",
            "sent_date",
        ]
