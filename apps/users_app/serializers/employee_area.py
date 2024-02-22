from django.contrib.auth import authenticate
from rest_framework import serializers

from apps.users_app.models import EmployeeArea


class EmployeeAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeArea
        fields = "__all__"
