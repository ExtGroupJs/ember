from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel

# TODO si cambia alguno de los elementos que intervienen en la restricción del unique,
# generar un nuevo producto.


class Production(BaseModel):
    name = models.CharField(max_length=30, verbose_name=_("Nombre"))
    product = models.ForeignKey(
        to="products_app.Product",
        on_delete=models.CASCADE,
        verbose_name=_("Producciones"),
        related_name="productions",
    )
    extra_info = models.TextField(
        verbose_name=_("Información Extra"), blank=True, null=True, max_length=256
    )

    plan = models.ForeignKey(
        to="products_app.Plan",
        on_delete=models.CASCADE,
        verbose_name=_("plan"),
        related_name="productions",
        null=True,
        default=None,
    )

    distribution_format = models.ForeignKey(
        to="products_app.GroupingPackaging",
        on_delete=models.PROTECT,
        verbose_name=_("Formato de distribución"),
        related_name="productions",
    )
    quantity = models.PositiveIntegerField(verbose_name=_("Cantidad"))
    cost = models.DecimalField(
        verbose_name=_("Costo"),
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0.00)],
        null=True,
        blank=True,
    )
    wholesale_price = models.DecimalField(
        verbose_name=_("Precio al por mayor"),
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0.00)],
    )
    active = models.BooleanField(verbose_name=_("Activo"), default=True)
    production_date = models.DateField(
        verbose_name=_("Fecha de producción"),
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("Producción")
        verbose_name_plural = _("Producciones")
        constraints = [
            models.constraints.UniqueConstraint(
                fields=["product", "distribution_format", "wholesale_price"],
                name="unique_product_format_and_major_price",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.name} ({self.product.name})-{self.distribution_format}"
