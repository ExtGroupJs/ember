from rest_framework import permissions, viewsets


from apps.common.views import CommonViewMixin
from apps.users_app.models import EmployeeArea
from apps.users_app.serializers.employee_area import EmployeeAreaSerializer

# Create your views here.


class EmployeeAreaViewSet(viewsets.ModelViewSet, CommonViewMixin):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = EmployeeArea.objects.all()
    serializer_class = EmployeeAreaSerializer

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    ordering = "name"
