from apps.common.filters import CommonFilter
import django_filters

from apps.products_app.models import Production


class ProductionFilter(CommonFilter):
    quantity_less_than = django_filters.NumberFilter(
        field_name="quantity", lookup_expr="lte"
    )
    quantity_more_than = django_filters.NumberFilter(
        field_name="quantity", lookup_expr="gte"
    )
    cost_less_than = django_filters.NumberFilter(field_name="cost", lookup_expr="lte")
    cost_more_than = django_filters.NumberFilter(field_name="cost", lookup_expr="gte")
    production_date_after = django_filters.DateTimeFilter(
        field_name="production_date", lookup_expr="date__gte"
    )
    production_date_before = django_filters.DateTimeFilter(
        field_name="production_date", lookup_expr="date__lte"
    )

    class Meta:
        model = Production
        fields = [
            "product",
            "distribution_format",
            "plan__ueb",
            "plan__destiny",
            "plan",
        ]
