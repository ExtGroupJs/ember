import pytest
from django.core.management import call_command
from io import StringIO

from apps.products_app.models import Classification


def _make_cycle(*names):
    """Build a chain and close it so the first node points at the last one.

    Creates A -> B -> C, then sets A.parent = C, which yields the cycle
    A -> C -> B -> A. The newest node is the one that closed it.
    """
    nodes = []
    previous = None
    for name in names:
        node = Classification.objects.create(name=name, parent=previous)
        nodes.append(node)
        previous = node
    # close the cycle: the root now points at the newest node
    Classification.objects.filter(pk=nodes[0].pk).update(parent=previous)
    return nodes


def _has_cycle():
    """True when some node's parent chain never reaches a root."""
    parent_of = dict(Classification.objects.values_list("id", "parent_id"))
    for start in parent_of:
        seen = set()
        current = start
        while current is not None and current not in seen:
            seen.add(current)
            current = parent_of.get(current)
        if current is not None:
            return True
    return False


@pytest.mark.django_db
def test_command_reports_no_cycles_when_tree_is_valid():
    root = Classification.objects.create(name="root")
    Classification.objects.create(name="child", parent=root)
    out = StringIO()

    call_command("fix_classification_cycles", stdout=out)

    assert "No cycles found" in out.getvalue()


@pytest.mark.django_db
def test_command_breaks_two_node_cycle_on_the_newest_node():
    first, second = _make_cycle("cycle_a", "cycle_b")
    out = StringIO()

    call_command("fix_classification_cycles", stdout=out)

    # the newest node (highest id, the one that closed the cycle) becomes a root
    second.refresh_from_db()
    first.refresh_from_db()
    assert second.parent is None
    # the other edge survives, so the pair collapses into a valid parent/child
    assert first.parent == second
    assert not _has_cycle()
    assert "broken" in out.getvalue()


@pytest.mark.django_db
def test_command_breaks_three_node_cycle_on_the_newest_node():
    first, second, third = _make_cycle("a", "b", "c")
    out = StringIO()

    call_command("fix_classification_cycles", stdout=out)

    third.refresh_from_db()
    second.refresh_from_db()
    first.refresh_from_db()
    # the newest node is the one cut; every other edge is left alone
    assert third.parent is None
    assert second.parent == first
    assert first.parent == third
    assert not _has_cycle()


@pytest.mark.django_db
def test_command_breaks_self_parent_cycle():
    node = Classification.objects.create(name="self_parent")
    Classification.objects.filter(pk=node.pk).update(parent=node)
    out = StringIO()

    call_command("fix_classification_cycles", stdout=out)

    node.refresh_from_db()
    assert node.parent is None
    assert not _has_cycle()


@pytest.mark.django_db
def test_command_dry_run_does_not_write():
    _make_cycle("cycle_a", "cycle_b")
    before = dict(Classification.objects.values_list("id", "parent_id"))
    out = StringIO()

    call_command("fix_classification_cycles", "--dry-run", stdout=out)

    assert dict(Classification.objects.values_list("id", "parent_id")) == before
    assert _has_cycle()
    assert "would be broken" in out.getvalue()


@pytest.mark.django_db
def test_command_handles_two_independent_cycles():
    _make_cycle("a1", "a2")
    _make_cycle("b1", "b2")
    out = StringIO()

    call_command("fix_classification_cycles", stdout=out)

    assert not _has_cycle()
    assert "2 cycle(s) broken" in out.getvalue()


@pytest.mark.django_db
def test_command_leaves_valid_siblings_untouched():
    root = Classification.objects.create(name="root")
    left = Classification.objects.create(name="left", parent=root)
    right = Classification.objects.create(name="right", parent=root)

    call_command("fix_classification_cycles", stdout=StringIO())

    for node in (root, left, right):
        node.refresh_from_db()
    assert left.parent == root
    assert right.parent == root
