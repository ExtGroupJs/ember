from rest_framework import routers

from apps.products_app.views import (
    ClassificationViewSet,
    DestinationViewSet,
    EntityViewSet,
    GroupingPackagingViewSet,
    IndividualPackagingViewSet,
    MeasurementUnitViewSet,
    ProductionViewSet,
    ProductViewSet,
    PlanViewSet,
)
from apps.products_app.views.individual_packaging import (
    IndividualPackagingMaterialEnumsViewSet,
)

router = routers.DefaultRouter()
router.register(r"product", ProductViewSet, basename="product")
router.register(r"plan", PlanViewSet, basename="plan")
router.register(r"production", ProductionViewSet, basename="production")
router.register(r"classification", ClassificationViewSet, basename="classification")
router.register(r"destination", DestinationViewSet, basename="destination")
router.register(r"entity", EntityViewSet, basename="entity")
router.register(
    r"grouping-packaging", GroupingPackagingViewSet, basename="grouping-packaging"
)
router.register(
    r"individual-packaging", IndividualPackagingViewSet, basename="individual-packaging"
)
router.register(
    r"individual-packaging-material",
    IndividualPackagingMaterialEnumsViewSet,
    basename="individual-packaging-material",
)
router.register(
    r"measurement-unit", MeasurementUnitViewSet, basename="measurement-unit"
)

urlpatterns = []

urlpatterns += router.urls
