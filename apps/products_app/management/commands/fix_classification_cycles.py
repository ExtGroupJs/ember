"""Detect and break cycles in ``Classification.parent``.

A cycle in the self-referencing tree used to surface as a ``RecursionError`` on
``GET /admin/products_app/product/`` (see issue #28). The model now refuses to
save a cycle, but data written before that validation still needs cleaning up.

The repair always cuts the edge on the most recently created node of the cycle,
since that is the one that closed it.
"""

from django.core.management.base import BaseCommand

from apps.products_app.models import Classification


class Command(BaseCommand):
    help = "Detect cycles in Classification.parent and break them on the newest node"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Only report the cycles that would be broken, without writing.",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        cycles = self._find_cycles()

        if not cycles:
            self.stdout.write(self.style.SUCCESS("No cycles found in Classification."))
            return

        for cycle in cycles:
            node = self._newest_of(cycle)
            others = ", ".join(
                f"#{item.pk} {item.name}" for item in cycle if item.pk != node.pk
            )
            self.stdout.write(
                self.style.WARNING(
                    f"Cycle of {len(cycle)} nodes: {others}, #{node.pk} {node.name}"
                )
            )
            self.stdout.write(
                f"  -> breaking the edge #{node.pk} {node.name} "
                f"(parent #{node.parent_id} -> NULL)"
            )
            if not dry_run:
                # Update by pk to bypass the cycle-rejecting model validation
                # this very command exists to clean up.
                Classification.objects.filter(pk=node.pk).update(parent=None)

        verb = "would be broken" if dry_run else "broken"
        self.stdout.write(self.style.SUCCESS(f"{len(cycles)} cycle(s) {verb}."))

    def _find_cycles(self):
        """Return every distinct cycle, each as a list of Classification nodes.

        Walks each node's parent chain, and whenever a chain revisits a node it
        has found a cycle, so the visited set is keyed by node to avoid
        reporting the same cycle once per member.
        """
        parent_of = dict(
            Classification.objects.values_list("id", "parent_id").iterator()
        )
        cycles = []
        reported = set()
        for start_id in parent_of:
            if parent_of[start_id] is None:
                continue
            chain = []
            position = {}
            current_id = start_id
            while current_id is not None and current_id not in position:
                position[current_id] = len(chain)
                chain.append(current_id)
                current_id = parent_of.get(current_id)
            if current_id is None:
                continue
            # current_id closes a cycle: everything from where it first appeared.
            cycle_ids = chain[position[current_id] :]
            # The same cycle is reachable from each of its members, so key on
            # the whole membership set rather than on the entry node.
            fingerprint = frozenset(cycle_ids)
            if fingerprint in reported:
                continue
            reported.add(fingerprint)
            cycles.append(list(Classification.objects.filter(pk__in=cycle_ids)))
        return cycles

    def _newest_of(self, cycle):
        """Return the most recently created node of the cycle.

        ``Classification`` has no creation timestamp, so the primary key stands
        in for insertion order on every table this project has populated
        through its migrations. The command reports the pk it acted on so the
        choice stays auditable.
        """
        newest_pk = max(node.pk for node in cycle)
        newest = next(node for node in cycle if node.pk == newest_pk)
        self.stdout.write(
            f"  (breaking on the highest id, the last one added: #{newest.pk})"
        )
        return newest
