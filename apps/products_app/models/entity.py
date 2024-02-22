from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class Entity(models.Model):
    name = models.CharField(max_length=30, verbose_name=_("name"), unique=True)
    email = models.EmailField(verbose_name=_("email"), unique=True)
    enabled = models.BooleanField(verbose_name=_("enabled"), default=True)
    phone_1 = models.CharField(
        verbose_name=_("phone number 1"),
        max_length=11,
        null=True,
        blank=True,
        validators=[
            RegexValidator(regex=r"^\+?\d+$", message="Only numeric characters allowed")
        ],
    )
    phone_2 = models.CharField(
        verbose_name=_("phone number 2"),
        max_length=11,
        null=True,
        blank=True,
        validators=[
            RegexValidator(regex=r"^\+?\d+$", message="Only numeric characters allowed")
        ],
    )

    class Meta:
        verbose_name = _("UEB")
        verbose_name_plural = _("UEBs")
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name
