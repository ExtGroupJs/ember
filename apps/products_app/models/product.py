from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel
from apps.products_app.models import Classification, Format


class Product(BaseModel):
    name = models.CharField(max_length=30, verbose_name=_("name"))
    format = models.ForeignKey(
        to=Format, on_delete=models.DO_NOTHING, null=True, blank=True
    )
    description = models.TextField(
        verbose_name=_("description"), blank=True, null=True, max_length=256
    )
    classification = models.ForeignKey(to=Classification, on_delete=models.PROTECT)

    class Meta:
        verbose_name = _("producto")
        verbose_name_plural = _("productos")

    def __str__(self) -> str:
        return f"{self.name} ({self.classification})"
