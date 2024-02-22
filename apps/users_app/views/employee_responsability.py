from rest_framework import permissions, viewsets


from apps.common.views import CommonViewMixin
from apps.users_app.models import EmployeeResponsability
from apps.users_app.serializers.employee_responsability import (
    EmployeeResponsabilitySerializer,
)

# Create your views here.


class EmployeeResponsabilityViewSet(viewsets.ModelViewSet, CommonViewMixin):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = EmployeeResponsability.objects.all()
    serializer_class = EmployeeResponsabilitySerializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    ordering = "name"
