from rest_framework import permissions, viewsets

from apps.common.views import CommonViewMixin
from apps.products_app.filters.classification import ClassificationFilter
from apps.products_app.models import Classification
from apps.products_app.serializers import ClassificationSerializer


class ClassificationViewSet(viewsets.ModelViewSet, CommonViewMixin):
    queryset = Classification.objects.all()
    serializer_class = ClassificationSerializer
    search_fields = ["name", "description"]
    filterset_class = ClassificationFilter
    ordering = ["id"]

    permission_classes = [permissions.IsAuthenticated]
