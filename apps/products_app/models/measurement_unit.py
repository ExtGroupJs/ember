from django.db import models
from django.utils.translation import gettext_lazy as _

ARCHIVED_FOR_RELATED_OBJECT = "Archived due to related object "


class MeasurementUnit(models.Model):
    name = models.CharField(max_length=20, verbose_name=_("name"), unique=True)
    symbol = models.CharField(
        max_length=10,
        verbose_name=_("symbol"),
        unique=True,
    )
    description = models.TextField(
        verbose_name=_("description"), blank=True, null=True, max_length=256
    )
    mililiters = models.PositiveIntegerField(
        verbose_name=_("mililiters"),
    )
    used_for_planning = models.BooleanField(
        default=False,
        verbose_name=_("used for planning"),
    )

    class Meta:
        verbose_name = _("unidad de medida")
        verbose_name_plural = _("unidades de medida")

    def __str__(self) -> str:
        return f"{self.name} ({self.symbol})"

    def convert_to(self, measurement_unit):
        pass

