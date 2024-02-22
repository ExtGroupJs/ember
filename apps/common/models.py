from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.common.get_username import current_request


class HistoricalVault(models.Model):
    deletion_timestamp = models.DateTimeField(
        _("Deletion timestamp"),
    )
    deletion_cause = models.TextField(_("deletion cause"), null=True, blank=True)
    author = models.ForeignKey(User, verbose_name=_("Author"), on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Historical Vault"
        verbose_name_plural = "Historical Vaults"

    def __str__(self) -> str:
        return f"{self.deletion_timestamp}"


class BaseModel(models.Model):
    created_timestamp = models.DateTimeField(verbose_name=_("Created timestamp"), auto_now_add=True)
    updated_timestamp = models.DateTimeField(verbose_name=_("Updated timestamp"), auto_now=True, null=True)
    historical_vault = models.ForeignKey(HistoricalVault, verbose_name=_("NOT USED"), on_delete=models.SET_NULL, null=True)

    class Meta:
        abstract = True

    def archive(self, *args, **kwargs):
        if not self.historical_vault:
            self.historical_vault = HistoricalVault.objects.create(
                deletion_timestamp=timezone.now(), author=current_request().user if current_request() else None, **kwargs
            )
        if kwargs.get("deletion_cause") is not None:
            kwargs.pop("deletion_cause")
        super().save(*args, **kwargs)
    
    def des_archive(self, *args, **kwargs):
        if self.historical_vault:
            self.historical_vault.delete()
    
    def is_active(self, *args, **kwargs):
        return self.historical_vault is None
