from django.db import models
from django.utils.translation import gettext_lazy as _


from apps.common.models import BaseModel
from apps.products_app.models import (
    Destination,
    Entity,
    Classification,
    MeasurementUnit,
)


class Plan(BaseModel):
    """
    El plan se hace para cada UEB, producto, destino, mes.
    se dan en hectolitro y o miles de cajas
    valor (opcional Miles de pesos)
    """

    class Months(models.IntegerChoices):
        ENE = 1, _("Enero")
        FEB = 2, _("Febrero")
        MAR = 3, _("Marzo")
        ABR = 4, _("Abril")
        MAY = 5, _("Mayo")
        JUN = 6, _("Junio")
        JUL = 7, _("Julio")
        AGO = 8, _("Agosto")
        SEP = 9, _("Septiembre")
        OCT = 10, _("Octubre")
        NOV = 11, _("Noviembre")
        DIC = 12, _("Diciembre")

    name = models.CharField(max_length=256, verbose_name=_("Nombre"))
    ueb = models.ForeignKey(
        to=Entity,
        on_delete=models.PROTECT,
        null=True,
        default=None,
        blank=True,
        related_name="plans",
    )
    destiny = models.ForeignKey(
        to=Destination,
        on_delete=models.PROTECT,
        null=True,
        default=None,
        blank=True,
        related_name="plans",
    )
    product_kind = models.ForeignKey(
        to=Classification,
        on_delete=models.CASCADE,
        verbose_name=_("Tipo de producto"),
        related_name="plans",
    )
    year = models.PositiveSmallIntegerField(
        verbose_name=_("Año"),
    )
    jan_quantity = models.FloatField(verbose_name=_("Plan enero"), default=0)
    feb_quantity = models.FloatField(verbose_name=_("Plan febrero"), default=0)
    mar_quantity = models.FloatField(verbose_name=_("Plan marzo"), default=0)
    apr_quantity = models.FloatField(verbose_name=_("Plan abril"), default=0)
    may_quantity = models.FloatField(verbose_name=_("Plan mayo"), default=0)
    jun_quantity = models.FloatField(verbose_name=_("Plan junio"), default=0)
    jul_quantity = models.FloatField(verbose_name=_("Plan julio"), default=0)
    aug_quantity = models.FloatField(verbose_name=_("Plan agosto"), default=0)
    sep_quantity = models.FloatField(verbose_name=_("Plan septiembre"), default=0)
    oct_quantity = models.FloatField(verbose_name=_("Plan octubre"), default=0)
    nov_quantity = models.FloatField(verbose_name=_("Plan noviembre"), default=0)
    dec_quantity = models.FloatField(verbose_name=_("Plan diciembre"), default=0)

    measurement_unit = models.ForeignKey(
        to=MeasurementUnit,
        verbose_name=_("Unidad de medida"),
        on_delete=models.PROTECT,
        related_name="plans",
    )

    class Meta:
        verbose_name = _("plan")
        verbose_name_plural = _("planes")
        # constraints = [
        #     models.constraints.UniqueConstraint(
        #         fields=["product_kind", "year"],
        #         name="unique_product_year_in_plan",
        #     ),
        # ]

    def __str__(self) -> str:
        # TODO cual será realmenteel formato de salida.
        return f"{self.name} {self.year} ({self.product_kind.name}) - {self.ueb.name}"
