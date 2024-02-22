import random

import pytest
from django.urls import reverse
from model_bakery import baker
from rest_framework import status

from apps.common.models import HistoricalVault
from apps.products_app.models import (GroupingPackaging, IndividualPackaging,
                                      Production)


@pytest.mark.django_db
def test_archive_object_child_of_base_model_from_ep(client):
    individual_package = baker.make("products_app.IndividualPackaging")
    assert IndividualPackaging.objects.count() == 1
    assert IndividualPackaging.objects.get(pk=individual_package.pk).historical_vault is None

    base_url = reverse("individual-packaging-archive", args=[individual_package.pk])
    client.login(username="admin", password="1qazxsw2")
    response = client.post(base_url)
    assert response.status_code == status.HTTP_200_OK
    assert IndividualPackaging.objects.count() == 1
    assert IndividualPackaging.objects.get(pk=individual_package.pk).historical_vault is not None
    assert HistoricalVault.objects.count() == 1


@pytest.mark.django_db
def test_archive_objects_childs_of_base_model(client):
    quantity = random.randint(1, 100)
    baker.make("products_app.IndividualPackaging", _quantity=quantity)
    assert IndividualPackaging.objects.count() == quantity
    assert HistoricalVault.objects.count() == 0

    assert IndividualPackaging.objects.filter(historical_vault__isnull=True).count() == quantity
    individual_packagings = IndividualPackaging.objects.all()
    client.login(username="admin", password="1qazxsw2")
    for individual_package in individual_packagings:
        base_url = reverse("individual-packaging-archive", args=[individual_package.pk])
        response = client.post(base_url)
        assert response.status_code == status.HTTP_200_OK

    assert IndividualPackaging.objects.count() == quantity
    assert IndividualPackaging.objects.filter(historical_vault__isnull=True).count() == 0
    assert HistoricalVault.objects.count() == quantity


@pytest.mark.django_db
def test_archiving_with_comment(client):
    production = baker.make("products_app.Production")
    assert IndividualPackaging.objects.count() == 1
    client.login(username="admin", password="1qazxsw2")

    data = {"deletion_cause": "test"}
    base_url = reverse("product-archive", args=[production.pk])
    response = client.post(base_url, data=data)
    assert response.status_code == status.HTTP_200_OK
    assert HistoricalVault.objects.count() == 1
    assert HistoricalVault.objects.first().deletion_cause == data["deletion_cause"]


@pytest.mark.django_db
def test_archiving_with_comment_in_cascade(client):
    production = baker.make("products_app.Production")
    assert IndividualPackaging.objects.count() == 1
    client.login(username="admin", password="1qazxsw2")

    data = {"deletion_cause": "test"}
    base_url = reverse("individual-packaging-archive", args=[production.distribution_format.individual_packaging.pk])
    response = client.post(base_url, data=data)
    assert response.status_code == status.HTTP_200_OK
    assert HistoricalVault.objects.count() == 3

    # for historical_vault in HistoricalVault.objects.all():
    #     print("-------------------------------------------------")
    #     print(historical_vault.deletion_cause)


@pytest.mark.django_db
def test_cascade_archiving(client):
    quantity = random.randint(1, 100)
    baker.make("products_app.Production", _quantity=quantity)
    assert IndividualPackaging.objects.count() == quantity
    assert GroupingPackaging.objects.count() == quantity
    assert Production.objects.count() == quantity
    assert HistoricalVault.objects.count() == 0

    individual_packagings = IndividualPackaging.objects.all()
    client.login(username="admin", password="1qazxsw2")
    for individual_package in individual_packagings:
        base_url = reverse("individual-packaging-archive", args=[individual_package.pk])
        response = client.post(base_url)
        assert response.status_code == status.HTTP_200_OK
    assert IndividualPackaging.objects.filter(historical_vault__isnull=False).count() == quantity
    assert GroupingPackaging.objects.filter(historical_vault__isnull=False).count() == quantity
    assert Production.objects.filter(historical_vault__isnull=False).count() == quantity
    assert HistoricalVault.objects.count() == 3 * quantity
