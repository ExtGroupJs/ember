from django.contrib.auth import login, logout
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.common.views import CommonViewMixin
from apps.users_app.models import SystemUser
from apps.users_app.serializers.user_and_login import LoginSerializer, UserSerializer

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

# Create your views here.


class UserViewSet(viewsets.ModelViewSet, CommonViewMixin):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = SystemUser.objects.exclude(username="admin").order_by("-date_joined")
    serializer_class = UserSerializer
    filterset_fields = ["username", "gender", "area", "responsability"]
    search_fields = ["username", "email", "first_name", "last_name"]

    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.action in ["login", "logout"]:
            permission_classes = [permissions.AllowAny]

        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=["POST"])
    @extend_schema(
        description="Provides authentication using user and password combination",
        request=LoginSerializer,
        responses={202: UserSerializer},
    )
    def login(self, request):
        serializer = LoginSerializer(
            data=self.request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        serializer = UserSerializer(user.systemuser)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    @action(detail=False, methods=["GET"])
    @extend_schema(
        description="Desloguear al usuario",
        responses={202: "Todo ok"},
    )
    def logout(self, request):
        logout(request)
        return Response(
            "Deslogueado exitosamente al usuario", status=status.HTTP_202_ACCEPTED
        )
