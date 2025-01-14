from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel

ARCHIVED_FOR_RELATED_OBJECT = "Archived due to related object "


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
        "IndividualPackaging",
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
