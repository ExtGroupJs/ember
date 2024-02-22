from django.db import models
from django.utils.translation import gettext_lazy as _


class Format(models.Model):
    """
    Caja, a granel, Pomo, paquete
    """

    name = models.CharField(max_length=30, verbose_name=_("name"), unique=True)
    description = models.TextField(
        verbose_name=_("description"), blank=True, null=True, max_length=256
    )

    class Meta:
        verbose_name = _("formato")
        verbose_name_plural = _("formatos")

    def __str__(self) -> str:
        return self.name
