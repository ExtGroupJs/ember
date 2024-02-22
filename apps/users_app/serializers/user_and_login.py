from django.contrib.auth import authenticate
from rest_framework import serializers

from apps.common.serializers import BaseModelSerializer
from apps.users_app.models import SystemUser


class UserSerializer(BaseModelSerializer):
    # TODO solo se necesita en la vista: nombre completo, área, correo, teléfonos
    # TODO en la edición sí serían todos los campos.
    class Meta(BaseModelSerializer.Meta):
        model = SystemUser
        fields = BaseModelSerializer.Meta.fields + [
            "id",
            "username",
            "email",
            "get_full_name",
            "first_name",
            "last_name",
            "is_staff",
            "ci",
            "photo",
            "gender",
            "password",
            "area",
            "responsability",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            # 'ci': {'write_only': True},
            # "first_name": {"write_only": True},
            # "last_name": {"write_only": True},
            # 'email': {'write_only': True},
            "is_staff": {"write_only": True},
        }

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        if validated_data.get("password"):
            user.set_password(validated_data["password"])
            user.save()
        return user


class LoginSerializer(serializers.Serializer):
    """
    This serializer defines two fields for authentication:
      * username
      * password.
    It will try to authenticate the user with when validated.
    """

    username = serializers.CharField(label="Username", write_only=True)
    password = serializers.CharField(
        label="Password",
        # This will be used when the DRF browsable API is enabled
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
    )

    def validate(self, attrs):
        # Take username and password from request
        username = attrs.get("username")
        password = attrs.get("password")

        if username and password:
            # Try to authenticate the user using Django auth framework.
            user = authenticate(
                request=self.context.get("request"),
                username=username,
                password=password,
            )
            if not user:
                # If we don't have a regular user, raise a ValidationError
                msg = "Access denied: wrong username or password."
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = 'Both "username" and "password" are required.'
            raise serializers.ValidationError(msg, code="authorization")
        # We have a valid user, put it in the serializer's validated_data.
        # It will be used in the view.
        attrs["user"] = user
        return attrs
