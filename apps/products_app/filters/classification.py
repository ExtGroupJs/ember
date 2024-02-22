import django_filters

from apps.products_app.models import Classification


class ClassificationFilter(django_filters.FilterSet):

    class Meta:
        model = Classification
        fields = {"parent": ["isnull"],}
       
