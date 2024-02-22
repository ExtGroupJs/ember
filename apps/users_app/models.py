import os
import uuid

from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.utils._os import safe_join
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel

# Create your models here.


class EmployeeArea(models.Model):
    name = models.CharField(max_length=30, verbose_name=_("name"), unique=True)
    description = models.TextField(verbose_name=_("description"), max_length=256)

    class Meta:
        verbose_name = _("area")
        verbose_name_plural = _("areas")


class EmployeeResponsability(models.Model):
    name = models.CharField(max_length=30, verbose_name=_("name"), unique=True)
    description = models.TextField(verbose_name=_("description"), max_length=256)

    class Meta:
        verbose_name = _("responsability")
        verbose_name_plural = _("responsabilities")


def get_file_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}_{instance.id}.{ext}"
    return safe_join("static/media/", filename)


class SystemUser(
    User,
    BaseModel,
):
    class GENDER(models.TextChoices):
        MALE = "M", _("male")
        FEMALE = "F", _("female")

    ci = models.CharField(
        verbose_name=_("identification number"),
        max_length=11,
        unique=True,
    )
    photo = models.ImageField(
        verbose_name=_("photo"),
        upload_to="images/",
        null=True,
    )
    gender = models.CharField(
        _("gender"), choices=GENDER.choices, default=GENDER.MALE, max_length=1
    )
    area = models.ForeignKey(
        EmployeeArea,
        verbose_name=_("area or department"),
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    responsability = models.ForeignKey(
        EmployeeResponsability,
        verbose_name=_("responsability or main tasks"),
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
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

    class Meta(User.Meta):
        verbose_name = _("System user")
        verbose_name_plural = _("System users")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class SystemEmail(BaseModel):
    topic = models.CharField(verbose_name=_("topic"), max_length=30)
    text = models.TextField(verbose_name=_("text"), null=True, blank=True)
    attachment = models.FileField(
        verbose_name=_("attachment"), null=True, blank=True, upload_to="attachments/"
    )
    sent_date = models.DateTimeField(verbose_name=_("date"), auto_now_add=True)
    user = models.ForeignKey(User, verbose_name=_("user"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("System email")
        verbose_name_plural = _("System emails")

    def __str__(self):
        return f"{self.topic} - {self.user}"
