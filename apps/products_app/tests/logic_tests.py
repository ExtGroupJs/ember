import random

import pytest
from django.core.exceptions import ValidationError
from django.urls import reverse
from model_bakery import baker
from rest_framework import status

from apps.products_app.models import (
    Classification,
    GroupingPackaging,
    IndividualPackaging,
)


@pytest.mark.django_db
def test_creating_individual_packaging():
    quantity = random.randint(1, 100)
    individual_packages_created = baker.make(
        "products_app.IndividualPackaging", _quantity=quantity
    )
    assert IndividualPackaging.objects.count() == quantity
    for individual_package in individual_packages_created:
        individual_package.is_grouping_packaging = True
        individual_package.save()
    assert GroupingPackaging.objects.count() == quantity
    for individual_package in individual_packages_created:
        individual_package.is_grouping_packaging = False
        individual_package.save()
    assert GroupingPackaging.objects.count() == 0


@pytest.mark.django_db
def test_deleting_individual_packaging():
    quantity = random.randint(1, 100)
    baker.make(
        "products_app.IndividualPackaging",
        is_grouping_packaging=True,
        _quantity=quantity,
    )
    assert IndividualPackaging.objects.count() == quantity
    assert GroupingPackaging.objects.count() == quantity
    assert (
        IndividualPackaging.objects.filter(historical_vault__isnull=True).count()
        == quantity
    )
    assert (
        GroupingPackaging.objects.filter(historical_vault__isnull=True).count()
        == quantity
    )

    individual_packages = IndividualPackaging.objects.all()
    for individual_package in individual_packages:
        individual_package.archive()
    assert IndividualPackaging.objects.count() == quantity
    assert GroupingPackaging.objects.count() == quantity
    assert (
        IndividualPackaging.objects.filter(historical_vault__isnull=False).count()
        == quantity
    )
    assert (
        GroupingPackaging.objects.filter(historical_vault__isnull=False).count()
        == quantity
    )


@pytest.mark.django_db
def test_deleting_individual_packaging_not_allowed_if_is_used():
    quantity = random.randint(1, 100)
    individual_package = baker.make("products_app.IndividualPackaging")
    baker.make(
        "products_app.Production",
        distribution_format__individual_packaging=individual_package,
        _quantity=quantity,
    )
    assert GroupingPackaging.objects.count() == quantity
    assert IndividualPackaging.objects.count() == 1
    assert (
        IndividualPackaging.objects.filter(historical_vault__isnull=True).count() == 1
    )
    assert (
        GroupingPackaging.objects.filter(historical_vault__isnull=True).count()
        == quantity
    )
    with pytest.raises(Exception):
        individual_package.delete()
    assert GroupingPackaging.objects.count() == quantity
    assert IndividualPackaging.objects.count() == 1


@pytest.mark.django_db
def test_creating_grouping_packaging_from_individuals():
    quantity = random.randint(1, 100)
    baker.make(
        "products_app.IndividualPackaging",
        is_grouping_packaging=True,
        _quantity=quantity,
    )
    assert IndividualPackaging.objects.count() == quantity
    assert GroupingPackaging.objects.count() == quantity


@pytest.mark.django_db
def test_creating_clasification(client):
    client.login(username="admin", password="1qazxsw2")
    base_url = reverse("classification-list")

    clasifications_with_parents = Classification.objects.filter(
        parent__isnull=False
    ).count()
    url_with_filter = base_url + "?parent__isnull=False"
    response = client.get(url_with_filter)
    assert response.status_code == status.HTTP_200_OK
    results = response.json()["results"]
    assert clasifications_with_parents == len(results)
    # until here is checked the original classifications

    data = {"name": "test_classification"}
    response = client.post(base_url, data=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    # without parent the call should fail

    parent = Classification.objects.first()
    data["parent"] = parent.id
    response = client.post(base_url, data=data)
    assert response.status_code == status.HTTP_201_CREATED
    response = client.get(url_with_filter)
    assert response.status_code == status.HTTP_200_OK
    results = response.json()["results"]
    assert clasifications_with_parents + 1 == len(results)
    # the new classification is inserted in de db and correctly retrieved in the list


@pytest.mark.django_db
def test_classification_cannot_be_its_own_parent():
    classification = baker.make(Classification)
    classification.parent = classification
    with pytest.raises(ValidationError):
        classification.full_clean()


@pytest.mark.django_db
def test_classification_cannot_be_child_of_its_own_child():
    grandparent = baker.make(Classification)
    parent = baker.make(Classification, parent=grandparent)
    child = baker.make(Classification, parent=parent)

    grandparent.parent = child
    with pytest.raises(ValidationError):
        grandparent.full_clean()


@pytest.mark.django_db
def test_classification_allows_sibling_and_deeper_descendants():
    root = baker.make(Classification)
    other = baker.make(Classification)
    child = baker.make(Classification, parent=root)

    # a sibling is a valid parent
    other.parent = root
    other.full_clean()
    other.save()
    assert other.parent == root

    # a deeper descendant of another branch is still a cycle
    root.parent = child
    with pytest.raises(ValidationError):
        root.full_clean()


def _make_cycle():
    """Persist an A -> B -> A cycle, bypassing full_clean on purpose.

    Cycles predating the model validation can only be reproduced by writing
    parent_id directly, which is exactly how the bad data reached production.
    """
    first = baker.make(Classification, name="cycle_a")
    second = baker.make(Classification, name="cycle_b")
    Classification.objects.filter(pk=first.pk).update(parent=second)
    Classification.objects.filter(pk=second.pk).update(parent=first)
    return first, second


@pytest.mark.django_db
def test_str_does_not_recurse_on_cyclic_parent():
    first, _ = _make_cycle()
    first.refresh_from_db()

    # only guards the crash: a cycle has no meaningful hierarchy to render
    assert first.name in str(first)
    assert isinstance(str(first), str)


@pytest.mark.django_db
def test_str_full_hierarchy_does_not_recurse_on_cyclic_parent():
    first, _ = _make_cycle()
    first.refresh_from_db()

    assert first.name in first._str_full_hierarchy()


@pytest.mark.django_db
def test_get_all_children_recursively_terminates_on_cyclic_parent():
    first, second = _make_cycle()
    first.refresh_from_db()

    children = first.get_all_children_recursively()

    # the cycle must not produce duplicates nor an infinite walk
    assert len(children) == len({child.pk for child in children})
    assert {first.pk, second.pk} <= {child.pk for child in children}


@pytest.mark.django_db
def test_deep_hierarchy_is_still_rendered():
    root = baker.make(Classification, name="root")
    current = root
    for level in range(1, 5):
        current = baker.make(Classification, name=f"level_{level}", parent=current)

    assert str(current) == "----level_4"
    assert current._str_full_hierarchy() == "level_4 (root)"


@pytest.mark.django_db
def test_get_all_children_recursively_returns_full_branch():
    root = baker.make(Classification)
    first_child = baker.make(Classification, parent=root)
    second_child = baker.make(Classification, parent=root)
    grandchild = baker.make(Classification, parent=first_child)

    result = root.get_all_children_recursively()
    assert set(result) == {root, first_child, second_child, grandchild}
