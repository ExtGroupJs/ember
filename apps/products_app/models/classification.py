from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create a model called Clasification with two text fields

# Depth of the classification tree. The deepest hierarchy shipped by the
# migrations has 4 levels, so this leaves room while keeping a corrupted or
# cyclic parent chain from recursing without bound.
MAX_HIERARCHY_DEPTH = 20


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

    def clean(self):
        super().clean()
        if self.parent_id is None:
            return
        if self.pk is not None and self.parent_id == self.pk:
            raise ValidationError(
                {"parent": _("A classification cannot be its own parent.")}
            )
        if self._has_ancestor(self.parent_id):
            raise ValidationError(
                {
                    "parent": _(
                        "A classification cannot be a child of one of its own children."
                    )
                }
            )

    def _has_ancestor(self, ancestor_id, seen=None):
        """Walk up the parent chain looking for ``ancestor_id``.

        The walk is bounded in both directions: ``seen`` stops it from looping
        forever on already-corrupt data, and MAX_HIERARCHY_DEPTH keeps a very
        deep chain from exhausting the stack.
        """
        if seen is None:
            seen = set()
        current_id = ancestor_id
        for _step in range(MAX_HIERARCHY_DEPTH):
            if current_id in seen:
                return False
            seen.add(current_id)
            current_id = (
                Classification.objects.filter(pk=current_id)
                .values_list("parent_id", flat=True)
                .first()
            )
            if current_id is None:
                return False
            if self.pk is not None and current_id == self.pk:
                return True
        return False

    def __str__(self) -> str:
        return f"{self._hierarchy(self)}{self.name}"

    def _hierarchy(self, instance, seen=None):
        if seen is None:
            seen = set()
        if not instance.parent or self._is_revisited(instance, seen):
            return ""
        return f"-{self.parent._hierarchy(instance.parent, seen)}"

    def _str_full_hierarchy(self):
        if not self.parent:
            return self.name
        if self._is_revisited(self, set()):
            return self.name
        return f"{self.name} ({self._full_hierarchy(self, set())})"

    def _full_hierarchy(self, instance, seen=None):
        if seen is None:
            seen = set()
        if not instance.parent or self._is_revisited(instance, seen):
            return instance.name
        return f"{self.parent._full_hierarchy(instance.parent, seen)}"

    def _is_revisited(self, instance, seen):
        """Register ``instance`` and report whether it was already in the chain.

        The caller owns ``seen`` so every level of a walk shares one set; a fresh
        set per entry point keeps the public signatures unchanged.
        """
        if instance.pk in seen:
            return True
        seen.add(instance.pk)
        return False

    def get_all_children_recursively(self, parent_clasification=None, seen=None):
        if not parent_clasification:
            parent_clasification = self
        if seen is None:
            seen = set()
        if parent_clasification.pk in seen:
            return []
        seen.add(parent_clasification.pk)
        final_list = [parent_clasification]
        children = Classification.objects.filter(parent=parent_clasification)
        for child in children:
            final_list.extend(self.get_all_children_recursively(child, seen))
        return final_list
