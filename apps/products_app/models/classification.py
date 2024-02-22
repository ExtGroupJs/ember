from typing import final
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create a model called Clasification with two text fields


class Classification(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("name"), unique=True)
    description = models.TextField(
        verbose_name=_("description"), blank=True, null=True, max_length=256
    )
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, blank=True, null=True, default=None
    )

    class Meta:
        verbose_name = _("clasificación")
        verbose_name_plural = _("clasificaciones")

    def __str__(self) -> str:
        return f"{self._hierarchy(self)}{self.name}"

    def _hierarchy(self, instance):
        if instance.parent:
            return f"-{self.parent._hierarchy(instance.parent)}"
        return ""

    def _str_full_hierarchy(self):
        if self.parent:
            return f"{self.name} ({self._full_hierarchy(self)})"
        return self.name

    def _full_hierarchy(self, instance):
        if instance.parent:
            return f"{self.parent._full_hierarchy(instance.parent)}"
        return instance.name

    def get_all_children_recursively(self, parent_clasification=None):
        if not parent_clasification:
            parent_clasification = self
        final_list = [parent_clasification]
        children = Classification.objects.filter(parent=parent_clasification)
        for child in children:
            final_list.extend(self.get_all_children_recursively(child))
        return final_list
