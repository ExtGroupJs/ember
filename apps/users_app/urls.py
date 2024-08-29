from rest_framework import routers

from apps.users_app.views.employee_area import EmployeeAreaViewSet
from apps.users_app.views.employee_responsability import EmployeeResponsabilityViewSet
from apps.users_app.views.system_email import SystemEmailViewSet
from apps.users_app.views.users import UserViewSet

router = routers.DefaultRouter()
router.register(r"users", UserViewSet, basename="users")
router.register(r"system-email", SystemEmailViewSet, basename="system-email")
router.register(r"employee-area", EmployeeAreaViewSet, basename="area")
router.register(
    r"employee-responsability", EmployeeResponsabilityViewSet, basename="responsability"
)


urlpatterns = []

urlpatterns += router.urls
