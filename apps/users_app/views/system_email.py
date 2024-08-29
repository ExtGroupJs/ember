from rest_framework import permissions, viewsets


from apps.common.views import CommonViewMixin
from apps.users_app.models import SystemEmail
from apps.users_app.serializers.system_email import SystemEmailSerializer

# Create your views here.


class SystemEmailViewSet(viewsets.ModelViewSet, CommonViewMixin):
    """
    API endpoint that allows SystemEmail to be viewed or edited.
    """

    queryset = SystemEmail.objects.order_by("-sent_date")
    serializer_class = SystemEmailSerializer
    filterset_fields = ["user", "topic", "sent_date"]
    search_fields = ["user", "topic", "sent_date"]

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
