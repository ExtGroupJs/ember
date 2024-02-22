from django.db import models
from django.utils.translation import gettext_lazy as _


class Destination(models.Model):
    name = models.CharField(max_length=30, verbose_name=_("name"), unique=True)
    enabled = models.BooleanField(verbose_name=_("enabled"), default=True)

    class Meta:
        verbose_name = _("destino")
        verbose_name_plural = _("destinos")

    def __str__(self) -> str:
        return self.name
