from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel

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


class IndividualPackaging(BaseModel):
    class MATERIAL(models.TextChoices):
        PEP = "P", _("Plástico")
        VIDRIO = "V", _("Vidrio")

    name = models.CharField(max_length=30, verbose_name=_("name"), unique=True)
    description = models.TextField(
        verbose_name=_("description"), blank=True, null=True, max_length=256
    )
    capacity = models.DecimalField(
        verbose_name=_("capacity"),
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0.00)],
    )
    measurement_unit = models.ForeignKey(
        to=MeasurementUnit,
        on_delete=models.PROTECT,
        verbose_name=_("measurement unit"),
    )
    is_grouping_packaging = models.BooleanField(
        default=False, verbose_name=_("is grouping packaging")
    )
    material = models.CharField(
        verbose_name=_("Material"),
        max_length=1,
        choices=MATERIAL.choices,
        default=MATERIAL.VIDRIO,
    )

    class Meta:
        verbose_name = _("Tipo de embase")
        verbose_name_plural = _("Tipos de embases")

    def __str__(self) -> str:
        material = self.MATERIAL(self.material).label
        return (
            f"{self.name} de {self.capacity}{self.measurement_unit.symbol} ({material})"
        )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Call the "real" save() method.
        if self.is_grouping_packaging:
            if not GroupingPackaging.objects.filter(
                individual_packaging=self, capacity=1
            ).exists():
                GroupingPackaging.objects.create(
                    name=self.name,
                    description=self.description,
                    capacity=1,
                    individual_packaging=self,
                )
        else:
            GroupingPackaging.objects.filter(
                individual_packaging=self, capacity=1
            ).delete()

    def archive(self, *args, **kwargs):
        grouping_packages = self.grouping_packaging.all()
        for package in grouping_packages:
            package.archive(
                deletion_cause=f"{ARCHIVED_FOR_RELATED_OBJECT} "
                f"<IndividualPackaging: {self.id}>"
            )
        super().archive(*args, **kwargs)


class GroupingPackaging(BaseModel):
    name = models.CharField(max_length=30, verbose_name=_("name"), unique=True)
    description = models.TextField(
        verbose_name=_("description"), blank=True, null=True, max_length=256
    )
    capacity = models.PositiveSmallIntegerField(
        verbose_name=_("capacity"),
        validators=[MinValueValidator(1)],
    )
    individual_packaging = models.ForeignKey(
        IndividualPackaging,
        verbose_name=_("Individual packaging"),
        on_delete=models.CASCADE,
        related_name="grouping_packaging",
    )

    class Meta:
        verbose_name = _("Embalaje")
        verbose_name_plural = _("Embalajes")

    def __str__(self) -> str:
        return (
            f"{self.capacity} x {self.individual_packaging.capacity} "
            f"{self.individual_packaging.measurement_unit.symbol}"
        )

    def archive(self, *args, **kwargs):
        productions = self.productions.all()
        for production in productions:
            production.archive(
                deletion_cause=f"{ARCHIVED_FOR_RELATED_OBJECT} "
                f"<GroupingPackaging> {self.id}>"
            )
        super().archive(*args, **kwargs)
