from apps.common.filters import CommonFilter

from apps.products_app.models import Product


class ProductFilter(CommonFilter):
    class Meta:
        model = Product
        fields = [
            "format",
            "classification",
        ]
