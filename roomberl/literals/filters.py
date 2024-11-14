import django_filters

from .models import Hostel


class HostelFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(
        field_name="price", lookup_expr="gte", label="Minimum Price"
    )
    max_price = django_filters.NumberFilter(
        field_name="price", lookup_expr="lte", label="Maximum Price"
    )

    class Meta:
        model = Hostel
        fields = ["min_price", "max_price"]
