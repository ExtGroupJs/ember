from apps.common.filters import CommonFilter
import django_filters

from apps.products_app.models import GroupingPackaging


class GroupingPackagingFilter(CommonFilter):
    capacity_less_than = django_filters.NumberFilter(
        field_name="capacity", lookup_expr="lte"
    )
    capacity_more_than = django_filters.NumberFilter(
        field_name="capacity", lookup_expr="gte"
    )

    class Meta:
        model = GroupingPackaging
        fields = [
            "individual_packaging",
        ]
