import django_filters


class CommonFilter(django_filters.FilterSet):
    """
    This should be used as a base class for all filters
    """

    is_active = django_filters.BooleanFilter(
        field_name="historical_vault", lookup_expr="isnull"
    )
    deletion_cause = django_filters.CharFilter(
        field_name="historical_vault__deletion_cause", lookup_expr="icontains"
    )
    deleted_by = django_filters.CharFilter(
        field_name="historical_vault__author__username", lookup_expr="icontains"
    )
    created_after = django_filters.DateTimeFilter(
        field_name="created_timestamp", lookup_expr="date__gte"
    )
    created_before = django_filters.DateTimeFilter(
        field_name="created_timestamp", lookup_expr="date__lte"
    )
    updated_after = django_filters.DateTimeFilter(
        field_name="updated_timestamp", lookup_expr="date__gte"
    )
    updated_before = django_filters.DateTimeFilter(
        field_name="updated_timestamp", lookup_expr="date__lte"
    )
    deleted_after = django_filters.DateTimeFilter(
        field_name="historical_vault__deletion_timestamp", lookup_expr="date__gte"
    )
    deleted_before = django_filters.DateTimeFilter(
        field_name="historical_vault__deletion_timestamp", lookup_expr="date__lte"
    )
