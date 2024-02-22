from django.contrib.auth import authenticate
from rest_framework import serializers

from apps.users_app.models import EmployeeResponsability


class EmployeeResponsabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeResponsability
        fields = "__all__"
