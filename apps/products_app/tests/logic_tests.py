import random

import pytest
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
